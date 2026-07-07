# Data Sources — US Equity Research

> 10 source categories cho bất kỳ cổ phiếu Mỹ nào. **2 chế độ**: yfinance script (nhanh, structured) làm primary, WebFetch làm fallback. Đọc ở Phase 1.

## A. ⭐ PRIMARY: yfinance script (Python, fast, structured)

**Script**: `scripts/fetch_us_data.py` (chạy từ skill root)

**Install (1 lần)**:
```bash
pip install yfinance pandas
```

**Usage**:
```bash
# Single ticker
python3 scripts/fetch_us_data.py AAPL --range 2 --output json > aapl_data.json

# Multiple tickers
python3 scripts/fetch_us_data.py NVDA MSFT GOOGL --range 2 > all_data.json

# Output to stderr = progress, stdout = JSON
python3 scripts/fetch_us_data.py TSLA 2>progress.log > tsla_data.json
```

**Data trả về** (13 sections per ticker):
- `company` — name, sector, industry, business description
- `market_data` — current price, market cap, 52w high/low, shares, float, avg volume
- `ratios_current` — P/E TTM, forward P/E, PEG, P/B, P/S, EV/EBITDA, ROE, ROA, margin, beta, dividend yield, FCF yield
- `per_share` — EPS TTM/forward, book value, revenue/share, FCF/share
- `growth` — revenue/earnings growth YoY + QoQ
- `income_statement_annual` — full IS (5 years typically)
- `balance_sheet_annual` — full BS
- `cashflow_annual` — full CF statement
- `free_cash_flow_annual` — derived: OCF − capex per year
- `price_weekly` — 52 weeks OHLCV (cho technical ACTIVE)
- `price_daily` — ~2 years OHLCV (cho technical PROFILE 15 blocks)
- `analyst_targets` — mean/median/high/low price targets
- `top_institutional_holders` — top 10 from 13F

**Tested**: AAPL fetch = 13 sections, 53 weekly bars + 251 daily bars, 5 years IS/BS/CF, no errors. ~3 seconds runtime.

**Fallback khi yfinance fail** (rare):
- Yahoo rate-limit → retry after 30s, hoặc fallback WebFetch
- Ticker không có (OTC, mới IPO) → fallback WebFetch
- Data point thiếu (vd "targetMedianPrice") → flag null, WebFetch bổ sung

## B. SECONDARY: WebFetch-based sources (10 categories)

Khi yfinance thiếu data hoặc cần qualitative (filings text, news, analyst commentary):

### 1. SEC EDGAR — filings chính thức (HIGHQ)
- **URL**: `https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={TICKER}&type=10-K&dateb=&owner=include&count=10`
- **CIK lookup**: `https://www.sec.gov/files/company_tickers.json`
- **Use**: 10-K, 10-Q, 8-K, DEF 14A proxy
- **Note**: rate limit 10 req/sec, set User-Agent header

### 2. Company IR — earnings release (HIGHQ)
- **URL pattern**: `https://investor.{company}.com/`
- **Use**: quarterly press release, EPS GAAP/non-GAAP, guidance, segment color, RPO/backlog, CEO commentary

### 3. Yahoo Finance — supplementary (HIGHQ)
- **Quote page**: `https://finance.yahoo.com/quote/{TICKER}/` — cross-check market data
- **Chart API** (CORS-friendly nếu yfinance fail): `https://query2.finance.yahoo.com/v8/finance/chart/{TICKER}?range=2y&interval=1d`

### 4. Macrotrends — 10+ year history (MEDQ)
- **URL**: `https://www.macrotrends.net/stocks/charts/{TICKER}/{company-slug}/{metric}`
- **Use**: 10-year tables (revenue, op income, net income, EPS, OCF, FCF, debt, P/E, P/B, ROE, ROA)

### 5. StockAnalysis.com — fundamentals + ratios (MEDQ)
- **URL**: `https://stockanalysis.com/stocks/{TICKER}/financials/`
- **Use**: clean tables, ratios, forecasts (consensus EPS)

### 6. CNN Markets / Market Chameleon — current valuation (MEDQ)
- **CNN**: `https://www.cnn.com/markets/stocks/{TICKER}`
- **Market Chameleon**: `https://www.marketchameleon.com/Overview/{TICKER}/`

### 7. Credit rating agencies — Fitch, S&P, Moody's (HIGHQ khi free)
- **Fitch**: `https://www.fitchratings.com/research/corporate-finance/`
- **S&P**: `https://www.spglobal.com/ratings/en/regulatory/`
- **Moody's**: `https://www.moodys.com/`
- **Use**: rating, outlook, key concerns

### 8. Sell-side analyst aggregators (MEDQ)
- **TipRanks**: `https://www.tipranks.com/stocks/{TICKER}/forecast`
- **MarketBeat**: `https://www.marketbeat.com/stocks/NYSE:{TICKER}/forecast/`
- **Use**: consensus Buy/Hold/Sell %, average/median/high/low target, recent changes

### 9. Press / deal reporting (MEDQ, per-event)
- **Reuters**, **CNBC**, **AP**, **Fortune** (free)
- **WSJ**, **FT**, **Bloomberg**, **Barron's** (some paywall) — fallback to Reuters

### 10. Independent / specialist research (LOWQ-MEDQ)
- **SemiAnalysis**, **Stratechery**, **The Information**, **Deepwater AM**, **Substack ecosystem**

## C. Recommended Phase 1 workflow

```python
# 1. Try yfinance first (fast, structured)
import subprocess
result = subprocess.run(
    ["python3", "scripts/fetch_us_data.py", ticker, "--range", "2"],
    capture_output=True, text=True, cwd=skill_root
)
if result.returncode == 0:
    data = json.loads(result.stdout)
    # data has 13 sections: price, fundamentals, ratios, analyst targets
else:
    # yfinance failed → fallback WebFetch
    # dispatch subagents per data_sources.md categories 1-10
    pass

# 2. Bổ sung qualitative qua WebFetch (luôn cần):
#    - SEC 10-K filings (risk factors, MD&A, commitments footnote)
#    - Analyst notes (thesis, bull/bear)
#    - Press/news (recent catalysts)
#    - Independent research (SemiAnalysis, Stratechery nếu relevant)
```

**Ưu điểm**: yfinance lấy số liệu (price, financials, ratios) trong 3 giây; WebFetch chỉ cần cho qualitative (filings text, analyst commentary, news) — giảm 80% thời gian research.

## D. Fallback strategy

| If yfinance fail | Fallback |
|---|---|
| Yahoo rate-limited | Wait 30s retry, hoặc WebFetch stockanalysis.com |
| Ticker không có | WebFetch đa nguồn |
| Data point thiếu (vd median target) | WebFetch TipRanks/MarketBeat |

| If WebFetch blocked | Fallback |
|---|---|
| WSJ/FT/Bloomberg paywall | Reuters, CNBC, AP, Fortune |
| SEC EDGAR slow | StockAnalysis for filings summary |
| Macrotrends stale | 10-K direct |

### 1. SEC EDGAR — filings chính thức (HIGHQ)
- **URL**: `https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={TICKER}&type=10-K&dateb=&owner=include&count=10`
- **Alternative direct**: `https://www.sec.gov/Archives/edgar/data/{CIK}/...`
- **Fetch**: 10-K (annual), 10-Q (quarterly), 8-K (current events), DEF 14A (proxy)
- **Use**: revenue, segment, OCF, capex, FCF, debt, cash, shares, RPO/backlog, commitments footnote, risk factors
- **Note**: SEC có rate limit — 10 requests/sec max. Set User-Agent header.
- **CIK lookup**: `https://www.sec.gov/files/company_tickers.json` (mapping TICKER → CIK)

### 2. Company IR — earnings release, investor day (HIGHQ)
- **URL pattern**: `https://investor.{company}.com/` (vd `investor.oracle.com`, `investor.apple.com`)
- **Use**: quarterly press release, EPS GAAP/non-GAAP, guidance, segment color, RPO/backlog disclosure, CEO commentary
- **Earnings call transcript**: Seeking Alpha, Motley Fool, or company IR webcast replay

### 3. Yahoo Finance — price + OHLCV (HIGHQ for price)
- **Chart API** (no key, CORS-friendly): `https://query2.finance.yahoo.com/v8/finance/chart/{TICKER}?range={1y|2y|5y}&interval={1d|1wk|1mo}`
  - Returns: timestamp, open, high, low, close, volume (adjusted for splits/dividends)
  - Use for: 52w high/low, current price, OHLCV weekly/daily for technical analysis
- **Quote page**: `https://finance.yahoo.com/quote/{TICKER}/` — market cap, P/E, EPS, dividend yield, beta
- **Cross-check**: stockanalysis.com, macrotrends for OHLCV confirmation

### 4. Macrotrends — 10+ year financial history (MEDQ)
- **URL**: `https://www.macrotrends.net/stocks/charts/{TICKER}/{company-slug}/{metric}`
- **Metrics**: revenue, gross-profit, operating-income, net-income, eps-earnings-per-share-diluted, free-cash-flow, long-term-debt, total-assets, operating-cash-flow, pe-ratio, pb-ratio, ps-ratio, roe, roa
- **Use**: 10-year history tables (export-friendly format)
- **Caveat**: aggregator — cross-check với 10-K cho năm gần nhất. Older years có thể stale.

### 5. StockAnalysis.com — fundamentals + ratios (MEDQ)
- **URL**: `https://stockanalysis.com/stocks/{TICKER}/financials/`
- **Sections**: financials (annual/quarterly), balance-sheet, cash-flow-statement, ratios, forecast
- **Use**: clean tables, faster than Macrotrends cho ratios (P/E, P/B, EV/EBITDA, ROE, margin)
- **Forecasts**: consensus analyst estimates (revenue, EPS)

### 6. CNN Markets / Market Chameleon — current valuation (MEDQ)
- **CNN**: `https://www.cnn.com/markets/stocks/{TICKER}` — current price, market cap, P/E, dividend yield, 52w range
- **Market Chameleon**: `https://www.marketchameleon.com/Overview/{TICKER}/` — P/E, P/B, implied volatility, options data
- **Use**: real-time-ish valuation snapshot. Cross-check P/E vs Macrotrends (thường chênh 1-3× do TTM lag).

### 7. Credit rating agencies — Fitch, S&P, Moody's (HIGHQ when free)
- **Fitch**: `https://www.fitchratings.com/research/corporate-finance/` (search company)
- **S&P**: `https://www.spglobal.com/ratings/en/regulatory/` (search)
- **Moody's**: `https://www.moodys.com/`
- **Use**: credit rating, outlook (positive/stable/negative), key concerns
- **Caveat**: full reports paywalled; press releases free.

### 8. Sell-side analyst aggregators (MEDQ)
- **TipRanks**: `https://www.tipranks.com/stocks/{TICKER}/forecast` — consensus rating, price target distribution, analyst by analyst
- **MarketBeat**: `https://www.marketbeat.com/stocks/NYSE/{TICKER}/forecast/` — analyst count, consensus, recent upgrades/downgrades
- **CNN Business**: `https://www.cnn.com/markets/stocks/{TICKER}/forecasts` — simpler
- **Use**: consensus Buy/Hold/Sell %, average/median/high/low 12-month target, recent rating changes

### 9. Press / deal reporting (MEDQ, per-event)
- **WSJ**: `https://www.wsj.com/` (some paywall) — M&A, deal reporting
- **Reuters**: `https://www.reuters.com/` (free) — earnings, deal news
- **Bloomberg**: `https://www.bloomberg.com/` (paywall) — deep analysis
- **FT**: `https://www.ft.com/` (paywall) — strategic analysis
- **CNBC**: `https://www.cnbc.com/` (free) — market reaction, analyst interviews
- **Barron's**: `https://www.barrons.com/` (some paywall)
- **AP / NYT / Fortune**: supplementary
- **Use**: deal news (contract announcements, M&A, leadership change), earnings reaction context, bear/bull thesis articulation

### 10. Independent / specialist research (LOWQ-MEDQ, per-thesis)
- **SemiAnalysis** (substack) — semis/AI infra deep dives
- **Stratechery** (Ben Thompson) — tech strategy
- **The Information** — tech company internals (paywall)
- **Deepwater Asset Management** (Gene Munster) — tech commentary
- **Seeking Alpha** — crowd-sourced bull/bear articles (variable quality)
- **Substack ecosystem** — niche analysts per industry
- **Use**: independent thesis articulation, data points sell-side misses

## B. Fallback strategy

| If source blocked | Fallback |
|---|---|
| WSJ/FT/Bloomberg paywall | Reuters, CNBC, AP, Fortune (free) |
| Yahoo Finance API rate-limited | stockanalysis.com, macrotrends |
| SEC EDGAR slow | StockAnalysis for filings summary |
| Macrotrends stale (older year) | 10-K PDF direct from SEC |
| Analyst aggregators stale | Press search for recent upgrades/downgrades |

## C. URL patterns cheatsheet

```
SEC EDGAR (CIK lookup):
  https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={TICKER}&type=10-K

Yahoo Finance (price/OHLCV):
  https://query2.finance.yahoo.com/v8/finance/chart/{TICKER}?range=2y&interval=1d

Macrotrends (10y history):
  https://www.macrotrends.net/stocks/charts/{TICKER}/{company-slug}/{metric}

StockAnalysis (fundamentals):
  https://stockanalysis.com/stocks/{TICKER}/financials/

TipRanks (analyst):
  https://www.tipranks.com/stocks/{TICKER}/forecast
```

## D. Multi-source discrepancy handling

When sources disagree (common):
- P/E: Macrotrends vs StockAnalysis vs Market Chameleon — range thường 2-5×. Report midpoint + range, flag as MEDQ.
- EPS: GAAP vs non-GAAP gap large (case ORCL: 31%). Specify which.
- Net income: derived (EPS × shares) vs reported — flag if derived.
- Debt: "long-term debt" (Macrotrends) vs "notes payable + other borrowings" (10-K) — different scope, report both.

See `references/data_pitfalls.md` for 7 traps.
