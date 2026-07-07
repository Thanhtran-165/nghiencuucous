#!/usr/bin/env python3
"""
preflight.py — Kiểm tra cổ phiếu TRƯỚC khi chạy pipeline us-equity-research.

Chạy ~3 giây. Trả JSON có:
  - ticker, company_name, sector
  - flags: list các vấn đề cần user biết TRƯỚC khi build báo cáo
  - recommendations: path đề xuất (vd "dùng EV/Revenue thay P/E")
  - go_no_go: "GO" (chạy tiếp) | "WARN" (chạy tiếp nhưng flag) | "STOP" (hỏi user)

Mục đích: chống silent failure — 3 case vỡ rõ:
  1. Công ty lỗ (EPS TTM ≤ 0) → P/E vô nghĩa, cần path khác
  2. ADR / ngoại tệ (currency != USD) → flag, không lẫn đơn vị
  3. IPO/recent listing (history < period yêu cầu) → flag, đề xuất giảm period
  4. Ticker có dấu chấm (BRK.B) → sanitize folder name
  5. Penny stock / illiquid (market cap < $100M) → flag

Usage:
  python3 preflight.py TICKER [--period 10y]
  python3 preflight.py SNOW
  python3 preflight.py NVO
  python3 preflight.py BRK.B
"""

import sys
import json
import argparse
from datetime import datetime, date

try:
    import yfinance as yf
except ImportError:
    print("ERROR: yfinance not installed. pip install yfinance", file=sys.stderr)
    sys.exit(2)


def preflight(ticker: str, period_years: int = 10) -> dict:
    """Chạy preflight checks cho 1 ticker. Trả dict có flags + go_no_go."""
    t = yf.Ticker(ticker)
    info = t.info or {}

    result = {
        "ticker": ticker.upper(),
        "checked_at": datetime.now().isoformat(),
        "company_name": info.get("longName") or info.get("shortName") or "NOT FOUND",
        "sector": info.get("sector"),
        "industry": info.get("industry"),
        "exchange": info.get("exchange"),
        "currency": info.get("currency", "USD"),
        "country": info.get("country"),
        "flags": [],
        "recommendations": [],
        "go_no_go": "GO",
    }

    # === Check 1: NEGATIVE EARNINGS (P/E vô nghĩa) ===
    eps_ttm = info.get("trailingEps")
    pe_ttm = info.get("trailingPE")
    if eps_ttm is not None and eps_ttm <= 0:
        result["flags"].append({
            "id": "NEGATIVE_EARNINGS",
            "severity": "WARN",
            "msg": f"EPS TTM = ${eps_ttm:.2f} (âm). P/E TTM vô nghĩa (hoặc None).",
            "impact": "Section Valuation (8) sẽ vỡ: không có P/E percentile, không có 3-zone verdict. "
                      "Định giá bằng P/E misleading.",
            "fix": "Đổi sang EV/Revenue + EV/Gross Profit + Rule of 40 (growth % + margin %). "
                   "Flag clear trong báo cáo: 'Công ty đang trong giai đoạn tăng trưởng, P/E không áp dụng.'"
        })
        result["recommendations"].append(
            "Valuation path B (growth/IPO): dùng EV/Revenue + EV/Gross Profit + Rule of 40 thay P/E."
        )
    elif pe_ttm is None and eps_ttm is None:
        result["flags"].append({
            "id": "EPS_NOT_AVAILABLE",
            "severity": "WARN",
            "msg": "EPS TTM = None (Yahoo không trả). Không biết công ty có lãi không.",
            "impact": "Valuation section không xác định được path A (P/E) hay path B (EV/Revenue).",
            "fix": "Verify EPS qua SEC 10-K trước khi chọn valuation path."
        })

    # === Check 2: FOREIGN CURRENCY / ADR ===
    # 2 tầng: currency field HOẶC country field (Yahoo có thể đã convert ADR sang USD)
    currency = info.get("currency", "USD")
    country = info.get("country", "United States")
    is_foreign = currency != "USD" or (
        country not in ("United States", "USA", None)
    )
    if is_foreign:
        currency_detail = f"currency={currency}" if currency != "USD" else f"country={country} (ADR — Yahoo đã convert sang USD)"
        result["flags"].append({
            "id": "FOREIGN_CURRENCY_OR_ADR",
            "severity": "WARN",
            "msg": f"Công ty nước ngoài ({currency_detail}). Báo cáo tài chính gốc có thể KHÔNG phải USD.",
            "impact": "ADR (NVO, ASML, TSM, BABA): price/market cap = USD trên sàn Mỹ, NHƯNG "
                      "financials gốc trong 10-K/annual report = local currency (DKK, EUR, TWD, CNY). "
                      "Yahoo có thể convert sẵn (sai tỷ giá) hoặc giữ local. Phải verify.",
            "fix": f"1) Check 10-K/IR: financials gốc bằng {currency if currency != 'USD' else 'local currency'}. "
                   f"2) Nếu khác USD → label RÕ ở mọi bảng. 3) So sánh Yahoo number vs 10-K — nếu lệch hệ số lớn → sai tỷ giá."
        })
        result["recommendations"].append(
            f"Verify financials gốc vs Yahoo. Flag ADR/foreign rõ ở hero."
        )

    # === Check 3: LISTING AGE vs PERIOD REQUESTED ===
    # yfinance trả "firstTradeDateEpochUtc" hoặc tìm trong price history
    first_trade = info.get("firstTradeDateEpochUtc")
    if first_trade:
        try:
            ipo_date = date.fromtimestamp(first_trade)
            years_listed = (date.today() - ipo_date).days / 365.25
            result["ipo_date"] = ipo_date.isoformat()
            result["years_listed"] = round(years_listed, 1)

            if years_listed < period_years:
                result["flags"].append({
                    "id": "HISTORY_TOO_SHORT",
                    "severity": "WARN",
                    "msg": f"Công ty IPO {ipo_date} (~{years_listed:.1f} năm) < period yêu cầu ({period_years} năm).",
                    "impact": f"Bảng Financial History chỉ có {int(years_listed)} năm thay vì {period_years}. "
                              f"Percentile 5Y/10Y có thể không đủ mẫu.",
                    "fix": f"Đề xuất giảm period xuống {max(3, int(years_listed))} năm. "
                           f"Flag rõ: 'Lịch sử chỉ {int(years_listed)} năm do IPO gần đây.'"
                })
                result["recommendations"].append(
                    f"Switch --period {max(3, int(years_listed))}y do IPO gần đây."
                )
        except (ValueError, OSError):
            pass
    else:
        # Fallback: check income_stmt history
        try:
            inc = t.income_stmt
            if inc is not None and not inc.empty:
                years_in_data = len(inc.columns)
                if years_in_data < period_years:
                    result["flags"].append({
                        "id": "HISTORY_INCOMPLETE",
                        "severity": "INFO",
                        "msg": f"yfinance chỉ trả {years_in_data} năm history (yêu cầu {period_years}).",
                        "impact": f"Bảng Financial History sẽ thiếu {period_years - years_in_data} năm.",
                        "fix": f"Bổ sung qua Macrotrends/10-K cho older years, hoặc flag 'history limited to {years_in_data}y'."
                    })
        except Exception:
            pass

    # === Check 4: TICKER SANITIZATION (BRK.B, BRK-B, BF.B) ===
    if "." in ticker or "-" in ticker:
        sanitized = ticker.upper().replace(".", "-").replace(" ", "-")
        result["flags"].append({
            "id": "TICKER_HAS_SPECIAL_CHAR",
            "severity": "INFO",
            "msg": f"Ticker '{ticker}' chứa dấu. Folder name CẦN sanitize.",
            "impact": "Folder 'brk.b-deploy' có dấu chấm — Vercel/filesystem có thể reject.",
            "fix": f"Folder: {sanitized.lower()}-deploy. Ticker trong yfinance giữ nguyên '{ticker}'."
        })
        result["folder_name"] = f"{sanitized.lower()}-deploy"
    else:
        result["folder_name"] = f"{ticker.lower()}-deploy"

    # === Check 5: ILLIQUID / PENNY STOCK ===
    market_cap = info.get("marketCap")
    if market_cap and market_cap < 100_000_000:  # < $100M
        result["flags"].append({
            "id": "ILLIQUID_SMALL_CAP",
            "severity": "WARN",
            "msg": f"Market cap ${market_cap/1e6:.0f}M (< $100M). Cổ phiếu nhỏ, thanh khoản thấp.",
            "impact": "Giá có thể volatile, spread rộng, data Yahoo có thể ít update. "
                      "Technical analysis PROFILE không đáng tin.",
            "fix": "Flag rõ trong báo cáo. Cân nhắc không chạy technical PROFILE."
        })

    # === Check 6: yfinance DATA AVAILABILITY (silent failure detection) ===
    critical_fields = ["trailingEps", "currentPrice", "marketCap", "longName"]
    missing = [f for f in critical_fields if info.get(f) is None]
    if missing:
        result["flags"].append({
            "id": "YFINANCE_DATA_MISSING",
            "severity": "WARN",
            "msg": f"yfinance thiếu {len(missing)} field quan trọng: {missing}",
            "impact": "Có thể yfinance fail im lặng. Nếu chạy tiếp, một số section sẽ có 'NOT FOUND'.",
            "fix": "Verify qua SEC EDGAR/WebFetch trước khi build. Có thể Yahoo đổi API."
        })

    # === Check 7: TICKER-NAME MISMATCH (silent failure khi ticker trùng tên symbol khác) ===
    # Casebook: ticker "GOLD" → yfinance trả "Gold.com, Inc." (KHÔNG phải Barrick Gold)
    #           Barrick đã rebrand GOLD → B (2025). User gõ "GOLD" mong đợi Barrick → SAI công ty.
    name = (info.get("longName") or info.get("shortName") or "").lower()
    website = (info.get("website") or "").lower()
    ticker_lower = ticker.lower()
    # Ticker là từ phổ biến → cao риск collision. Flag nếu:
    #   (a) name chứa ".com" / ".io" / ".net" (looks like domain, not blue-chip), HOẶC
    #   (b) market cap < $5B (blue-chip miners/energy thường >$20B)
    common_words_likely_ticker_collision = {
        "gold", "oil", "ai", "cash", "gain", "real", "fast", "play",
        "new", "best", "good", "save", "core", "data", "fund",
        "tech", "bio", "life", "work", "home", "care", "love", "app",
    }
    market_cap = info.get("marketCap", 0) or 0
    if ticker_lower in common_words_likely_ticker_collision:
        looks_like_domain = any(d in name for d in [".com", ".io", ".net", ".org", ".co"])
        small_cap = market_cap < 5_000_000_000
        if looks_like_domain or small_cap:
            result["flags"].append({
                "id": "TICKER_NAME_MISMATCH",
                "severity": "WARN",
                "msg": f"Ticker '{ticker}' là từ phổ biến → return '{info.get('longName') or info.get('shortName')}' "
                       f"(market cap ${market_cap/1e9:.1f}B). Có thể SAI công ty.",
                "impact": "Case 'GOLD' → yfinance trả 'Gold.com, Inc.' (KHÔNG phải Barrick Gold). "
                          "Barrick đã rebrand GOLD → B (2025). User tưởng phân tích Barrick nhưng thực ra công ty khác.",
                "fix": f"VERIFY: '{info.get('longName') or info.get('shortName')}' có phải công ty bạn muốn không? "
                       f"Website: {info.get('website', 'không có')}. "
                       f"Nếu muốn Barrick → ticker mới là 'B' (từ 2025)."
            })

    # === Check 8: BETA SANITY — REMOVED ===
    # Học từ NEM test (7/2026): territory bác bỏ map. Giả định "cyclical = beta >0.7" sai.
    # Energy 2026: XOM beta 0.16, COP 0.12, CVX 0.49 — beta thấp thật, không phải yfinance lỗi.
    # Check beta tạo nhiều false positive hơn true positive → bỏ.
    # Nếu cần verify beta, làm manual ở Phase 1, không automate.

    # === Determine GO / WARN / STOP ===
    warn_count = sum(1 for f in result["flags"] if f["severity"] == "WARN")
    if warn_count >= 3:
        result["go_no_go"] = "STOP"
    elif warn_count >= 1:
        result["go_no_go"] = "WARN"
    else:
        result["go_no_go"] = "GO"

    return result


def main():
    ap = argparse.ArgumentParser(description="Preflight check for us-equity-research")
    ap.add_argument("ticker", help="Ticker symbol (AAPL, SNOW, NVO, BRK.B)")
    ap.add_argument("--period", type=int, default=10, help="Period years requested (default 10)")
    args = ap.parse_args()

    result = preflight(args.ticker, args.period)
    print(json.dumps(result, indent=2, default=str, ensure_ascii=False))

    # Summary to stderr
    print(f"\n→ {args.ticker}: {result['go_no_go']} "
          f"({len(result['flags'])} flags: "
          f"{[f['id'] for f in result['flags']]})", file=sys.stderr)


if __name__ == "__main__":
    main()
