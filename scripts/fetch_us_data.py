#!/usr/bin/env python3
"""
fetch_us_data.py — Fetch US stock data via yfinance (fast, structured, free)
Usage: python3 fetch_us_data.py TICKER [TICKER2 ...] [--range 2y] [--output json|csv]

Output: structured JSON with price OHLCV, fundamentals, ratios, analyst data.
Fallback: nếu yfinance fail hoặc không có → exit nonzero, LLM dùng WebFetch (xem data_sources.md).

Requires: pip install yfinance pandas
  yfinance wraps Yahoo Finance API (no key needed).
"""

import sys
import json
import argparse
from datetime import datetime

try:
    import yfinance as yf
    import pandas as pd
except ImportError:
    print("ERROR: yfinance/pandas not installed. Install: pip install yfinance pandas", file=sys.stderr)
    print("Fallback: use WebFetch per references/data_sources.md", file=sys.stderr)
    sys.exit(2)


def fetch_ticker(ticker: str, range_years: int = 2) -> dict:
    """Fetch comprehensive data for one ticker. Returns dict; None fields = not available."""
    t = yf.Ticker(ticker)
    out = {"ticker": ticker.upper(), "fetched_at": datetime.now().isoformat(), "data_quality": {}}

    # === 1. INFO / COMPANY PROFILE ===
    try:
        info = t.info or {}
        out["company"] = {
            "name": info.get("longName") or info.get("shortName"),
            "sector": info.get("sector"),
            "industry": info.get("industry"),
            "country": info.get("country"),
            "exchange": info.get("exchange"),
            "currency": info.get("currency", "USD"),
            "website": info.get("website"),
            "employees": info.get("fullTimeEmployees"),
            "long_business": info.get("longBusinessSummary"),
        }
        out["market_data"] = {
            "current_price": info.get("currentPrice") or info.get("regularMarketPrice"),
            "market_cap": info.get("marketCap"),
            "enterprise_value": info.get("enterpriseValue"),
            "shares_outstanding": info.get("sharesOutstanding"),
            "float_shares": info.get("floatShares"),
            "52w_high": info.get("fiftyTwoWeekHigh"),
            "52w_low": info.get("fiftyTwoWeekLow"),
            "52w_change_pct": info.get("52WeekChange"),
            "avg_volume_10d": info.get("averageVolume10days"),
            "avg_volume": info.get("averageVolume"),
        }
        out["ratios_current"] = {
            "pe_ttm": info.get("trailingPE"),
            "pe_forward": info.get("forwardPE"),
            "peg_ratio": info.get("pegRatio"),
            "pb": info.get("priceToBook"),
            "ps_ttm": info.get("priceToSalesTrailing12Months"),
            "ev_ebitda": info.get("enterpriseToEbitda"),
            "ev_revenue": info.get("enterpriseToRevenue"),
            "profit_margins": info.get("profitMargins"),
            "gross_margins": info.get("grossMargins"),
            "operating_margins": info.get("operatingMargins"),
            "roe": info.get("returnOnEquity"),
            "roa": info.get("returnOnAssets"),
            "roi": info.get("returnOnInvestment"),
            "debt_to_equity": info.get("debtToEquity"),
            "current_ratio": info.get("currentRatio"),
            "quick_ratio": info.get("quickRatio"),
            "beta": info.get("beta"),
            "dividend_yield": info.get("dividendYield"),
            "payout_ratio": info.get("payoutRatio"),
            "fcf_yield": (info.get("freeCashflow") / info.get("marketCap")) if info.get("freeCashflow") and info.get("marketCap") else None,
        }
        out["per_share"] = {
            "eps_ttm": info.get("trailingEps"),
            "eps_forward": info.get("forwardEps"),
            "book_value": info.get("bookValue"),
            "revenue_per_share": info.get("revenuePerShare"),
            "fcf_per_share": info.get("freeCashflowPerShare", info.get("operatingCashflowPerShare")),
        }
        out["growth"] = {
            "revenue_growth_qq": info.get("revenueQuarterlyGrowth"),
            "revenue_growth_yy": info.get("revenueGrowth"),
            "earnings_growth": info.get("earningsGrowth"),
            "earnings_growth_qq": info.get("earningsQuarterlyGrowth"),
            "dividend_rate": info.get("dividendRate"),
        }
    except Exception as e:
        out["data_quality"]["info_error"] = str(e)

    # === 2. FINANCIALS — Annual (income, balance, cash flow) ===
    try:
        inc = t.income_stmt
        if inc is not None and not inc.empty:
            out["income_statement_annual"] = _df_to_records(inc)
    except Exception as e:
        out["data_quality"]["income_error"] = str(e)

    try:
        bs = t.balance_sheet
        if bs is not None and not bs.empty:
            out["balance_sheet_annual"] = _df_to_records(bs)
    except Exception as e:
        out["data_quality"]["balance_error"] = str(e)

    try:
        cf = t.cashflow
        if cf is not None and not cf.empty:
            out["cashflow_annual"] = _df_to_records(cf)
            # Derive FCF = OCF - Capex
            ocf = cf.loc["Operating Cash Flow"] if "Operating Cash Flow" in cf.index else None
            capex = cf.loc["Capital Expenditure"] if "Capital Expenditure" in cf.index else None
            if ocf is not None and capex is not None:
                fcf_dict = {}
                for col in cf.columns:
                    ocf_val = float(ocf[col]) if pd.notna(ocf[col]) else None
                    capex_val = float(capex[col]) if pd.notna(capex[col]) else None
                    if ocf_val is not None and capex_val is not None:
                        fcf_dict[str(col)] = {
                            "ocf": ocf_val, "capex": capex_val,
                            "fcf": ocf_val - capex_val
                        }
                    else:
                        fcf_dict[str(col)] = {
                            "ocf": ocf_val, "capex": capex_val,
                            "fcf": None,
                            "_note": "data missing (NaN) — flag as NOT VERIFIED"
                        }
                out["free_cash_flow_annual"] = fcf_dict
    except Exception as e:
        out["data_quality"]["cashflow_error"] = str(e)

    # === 3. QUARTERLY FINANCIALS (latest few quarters) ===
    try:
        inc_q = t.quarterly_income_stmt
        if inc_q is not None and not inc_q.empty:
            out["income_statement_quarterly"] = _df_to_records(inc_q)
    except Exception:
        pass

    # === 4. PRICE HISTORY — weekly + daily ===
    try:
        # Weekly ~52 weeks
        wk = t.history(period="1y", interval="1wk")
        if wk is not None and not wk.empty:
            out["price_weekly"] = _ohlc_to_records(wk)
    except Exception as e:
        out["data_quality"]["weekly_error"] = str(e)

    try:
        # Daily ~2 years
        dy = t.history(period=f"{range_years}y", interval="1d")
        if dy is not None and not dy.empty:
            out["price_daily"] = _ohlc_to_records(dy)
    except Exception as e:
        out["data_quality"]["daily_error"] = str(e)

    # === 5. ANALYST DATA ===
    try:
        rec = t.recommendations
        if rec is not None and not rec.empty:
            # Latest period recommendations
            out["analyst_recommendations_recent"] = rec.tail(10).to_dict("records") if hasattr(rec.tail(10), 'to_dict') else str(rec.tail(10))
    except Exception:
        pass

    try:
        rec_info = t.recommendations_info
        if rec_info is not None:
            out["analyst_recommendations_summary"] = str(rec_info)
    except Exception:
        pass

    try:
        # Analyst price targets
        info2 = t.info  # re-fetch (sometimes targets need separate)
        out["analyst_targets"] = {
            "mean": info2.get("targetMeanPrice"),
            "median": info2.get("targetMedianPrice"),
            "high": info2.get("targetHighPrice"),
            "low": info2.get("targetLowPrice"),
            "current": info2.get("currentPrice"),
        }
    except Exception:
        pass

    # === 6. INSTITUTIONAL HOLDERS (top 10) ===
    try:
        ih = t.institutional_holders
        if ih is not None and not ih.empty:
            out["top_institutional_holders"] = ih.head(10).to_dict("records")
    except Exception:
        pass

    # === 7. MAJOR HOLDERS % ===
    try:
        mh = t.major_holders
        if mh is not None and not mh.empty:
            out["major_holders_pct"] = str(mh)
    except Exception:
        pass

    # === DATA QUALITY SUMMARY ===
    sections_present = [k for k in ["company", "market_data", "ratios_current", "per_share", "growth",
                                     "income_statement_annual", "balance_sheet_annual", "cashflow_annual",
                                     "free_cash_flow_annual", "price_weekly", "price_daily",
                                     "analyst_targets", "top_institutional_holders"] if out.get(k)]
    out["data_quality"]["sections_present"] = sections_present
    out["data_quality"]["sections_count"] = len(sections_present)
    out["data_quality"]["errors"] = [k for k, v in out.get("data_quality", {}).items() if "_error" in k and v]

    return out


def _df_to_records(df):
    """Convert pandas DataFrame (columns = periods) to dict of period → {metric: value}."""
    result = {}
    for col in df.columns:
        period_str = str(col.date()) if hasattr(col, 'date') else str(col)
        result[period_str] = {}
        for idx in df.index:
            val = df.loc[idx, col]
            if pd.notna(val):
                try:
                    result[period_str][str(idx)] = float(val)
                except (ValueError, TypeError):
                    result[period_str][str(idx)] = str(val)
    return result


def _ohlc_to_records(df):
    """Convert OHLCV DataFrame to list of daily records."""
    records = []
    for idx, row in df.iterrows():
        rec = {
            "date": str(idx.date()) if hasattr(idx, 'date') else str(idx),
        }
        for col in ["Open", "High", "Low", "Close", "Volume"]:
            if col in row and pd.notna(row[col]):
                rec[col.lower()] = float(row[col])
        # Adj close if available
        if "Stock Splits" in row:
            rec["splits"] = float(row["Stock Splits"]) if pd.notna(row["Stock Splits"]) else 0
        records.append(rec)
    return records


def main():
    ap = argparse.ArgumentParser(description="Fetch US stock data via yfinance")
    ap.add_argument("tickers", nargs="+", help="Ticker symbol(s): NVDA AAPL MSFT")
    ap.add_argument("--range", type=int, default=2, dest="range_years", help="Daily history range in years (default 2)")
    ap.add_argument("--output", choices=["json", "csv"], default="json", help="Output format")
    args = ap.parse_args()

    for ticker in args.tickers:
        print(f"Fetching {ticker}...", file=sys.stderr)
        data = fetch_ticker(ticker, args.range_years)

        if args.output == "json":
            # allow_nan=False → NaN/Infinity thay bằng null (JSON strict compliant)
            # Tránh LLM đọc "NaN" và hiểu thành 0 (silent failure)
            print(json.dumps(data, indent=2, default=str, allow_nan=False))
        else:
            # Simple CSV: flatten one level
            for k1, v1 in data.items():
                if isinstance(v1, dict):
                    for k2, v2 in v1.items():
                        if not isinstance(v2, (dict, list)):
                            print(f"{ticker},{k1}.{k2},{v2}")

        # Per-ticker summary to stderr
        dq = data.get("data_quality", {})
        print(f"  → {ticker}: {dq.get('sections_count', 0)} sections, "
              f"{len(dq.get('errors', []))} errors", file=sys.stderr)


if __name__ == "__main__":
    main()
