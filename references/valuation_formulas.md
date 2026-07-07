# Valuation Formulas — US Equity

> Công thức + phương pháp định giá cổ phiếu Mỹ. Đọc ở Phase 3 (Section 5 history + Section 8 valuation).

## A. P/E & P/B — current vs 5Y/10Y avg/median

### Definitions
- **P/E TTM** = Price ÷ EPS diluted TTM (trailing twelve months, GAAP)
- **Forward P/E** = Price ÷ consensus EPS next FY (thường non-GAAP guidance)
- **P/B** = Price ÷ Book Value Per Share (BVPS = common equity ÷ diluted shares)
- **P/S** = Price ÷ Revenue Per Share = Market Cap ÷ Revenue TTM
- **EV/EBITDA** = Enterprise Value ÷ EBITDA TTM
  - EV = Market Cap + Total Debt - Cash & equivalents + Minority Interest + Preferred
- **FCF Yield** = FCF TTM ÷ Market Cap (HOẶC reciprocal của Price/FCF)

### 5Y/10Y averages — sources & method
| Source | URL | Coverage | Reliability |
|---|---|---|---|
| **Macrotrends** | `macrotrends.net/stocks/charts/{T}/{co}/pe-ratio` | 10+ year P/E | MEDQ (chart-based, ước tính) |
| **StockAnalysis** | `stockanalysis.com/stocks/{T}/ratios/` | 10+ year ratios | MEDQ |
| **Finbox** | `finbox.com/NYSE:{T}` | 10Y + forward | MEDQ |
| **GuruFocus** | `gurufocus.com/stock/{T}/summary` | 10Y + median | MEDQ |
| **FinanceCharts** | `financecharts.com/stock/{T}` | 10Y P/E | LOWQ |

**Method**: average và median khác nhau khi distribution skewed.
- Average = sum / N (sensitive to outliers — case ORCL FY25 P/E ~50× distorts avg)
- Median = middle value (robust — recommended primary)
- Report BOTH, nhưng default conclusion dùng median.

**Percentile calculation**:
```
sort P/E history ascending → rank current value → percentile = rank / N × 100
```
- < 25th percentile: historically cheap
- 25-75th: neutral
- > 75th: historically expensive

### P/B caveats with software/cloud companies
- **Buyback** reduces equity (treasury stock) → BVPS artificially low → P/B artificially high
- **Goodwill + intangibles** from acquisitions inflate book value → P/B artificially low (case ORCL: Cerner $28B goodwill)
- **Cloud capex** not yet depreciated inflates assets
- **Conclusion**: P/B with software/cloud = secondary indicator, NOT primary. Flag explicitly.

## B. DCF (Discounted Cash Flow) — 3 scenarios

### Free Cash Flow to Firm (FCFF)
```
FCFF = EBIT × (1 - tax rate) + D&A - capex - Δworking capital
```

### WACC
```
WACC = (E/V) × Re + (D/V) × Rd × (1 - tax rate)
  Re = cost of equity (CAPM: Rf + β × ERP)
  Rd = cost of debt (interest expense / debt)
  Rf = 10Y Treasury yield (~4-4.5% as of mid-2026)
  ERP = equity risk premium (~5-6%)
  β = beta vs S&P 500
```

### DCF formula
```
PV = Σ FCFF_t / (1 + WACC)^t  for t=1..N  +  Terminal Value / (1 + WACC)^N
Terminal Value = FCFF_{N+1} / (WACC - g)   where g = perpetual growth (2-3%)
```

### 3 scenarios
- **Bull**: high revenue growth, margin expansion, lower WACC
- **Base**: consensus growth, current margin, market WACC
- **Bear**: low growth, margin compression, higher WACC

**Caveat**: DCF với công ty FCF âm (case ORCL: −$23.7B FY26) gần như vô nghĩa — FCF âm → cần project khi nào FCF positive (FY28? FY29?). Flag honestly, hoặc skip DCF nếu không có FCF recovery model rõ.

## C. Other valuation methods

### EV/EBITDA
- Better than P/E cho công ty leverage cao, capex-heavy, hoặc có大 D&A
- Industry-specific norms (Energy 4-6×, Software 20-30×, Banks: not applicable)

### P/FCF (Price to Free Cash Flow)
- Better cho công ty có大 non-cash expenses (SBC, D&A)
- FCF yield = 1 / P/FCF
- **Caveat**: nếu FCF âm (case ORCL), P/FCF vô nghĩa. Flag.

### Reverse DCF
- Giả định current price = fair → back-out growth rate market is pricing
- Useful để trả lời "what growth is baked in?"

### Graham number
```
Graham Number = √(22.5 × EPS × BVPS)
```
- Conservative value floor (Buffett-style)
- Cho low-P/E, stable BVPS companies. Không dùng cho high-growth/software.

### Dividend Discount Model (DDM)
- Cho công ty dividend stable, mature (KO, JNJ, XOM)
- P0 = D1 / (r - g) where D1 = next year dividend, r = required return, g = dividend growth

## D. Sector-specific valuation choice

| Sector | Primary method | Why |
|---|---|---|
| **Software / Cloud** | P/S, EV/Revenue, P/FCF | FCF có thể âm; revenue growth matters more |
| **Tech / Semis** | P/E, PEG (P/E ÷ growth), EV/EBITDA | Profitable, growth-valued |
| **Internet / Ad** | P/E, EV/EBITDA | Cash-generative; growth premium |
| **Banks / Financial** | P/B, P/TBV (tangible book), ROE | Book value meaningful; tangible ex-goodwill |
| **Insurance** | P/B, combined ratio | Float-based business |
| **Healthcare / Pharma** | P/E, PEG, pipeline valuation | Patent cycle; earnings volatile |
| **Biotech** | Pipeline DCF, risk-adjusted NPV | Binary outcomes; revenue可能 zero |
| **Energy / Oil & Gas** | EV/EBITDA, P/CF (cash flow) | Commodity cycle; capex-heavy |
| **Utilities** | P/E, dividend yield, rate base growth | Regulated; bond-like |
| **REITs** | P/FFO (funds from operations), P/AFFO | Real estate specific metric |
| **Consumer / Retail** | P/E, EV/EBITDA, same-store sales growth | Margin + growth |
| **Auto / Industrial** | EV/EBITDA, P/FCF | Cyclical, capex-heavy |

## E. 3-zone valuation verdict (template)

| Zone | Condition | Meaning |
|---|---|---|
| **Comfort Zone** (green) | Current P/E near or below median lịch sử, growth xác nhận | Margin of safety relative |
| **Neutral Zone** (amber) | Current P/E above median, growth đang xác nhận | Có thể hợp lý nhưng cần theo dõi quarterly |
| **Danger Zone** (red) | Current P/E percentile cao + FCF âm + debt/capex tăng | Rủi ro multiple compression |

## F. Honest caveats (case ORCL applied)

1. **P/E thấp ≠ tự động rẻ** — Case ORCL: P/E ~24× thấp hơn 5Y avg ~35× NHƯNG EPS bị ép xuống bởi capex depreciation. "Rẻ" có thể là vì lý do chính đáng (earnings temporarily depressed).
2. **P/B cao ≠ tự động đắt** — Case ORCL: P/B ~10× nhưng buyback history giảm equity + Cerner goodwill phồng asset → méo. P/B chỉ tham khảo cho software/cloud.
3. **Forward P/E based on non-GAAP guidance** — có thể cut guidance. Always flag.
4. **FCF yield âm vô nghĩa** — không dùng nếu FCF âm.
5. **Cross-source discrepancy**: report range + midpoint, không bịa 1 số exact.

## G. Output format (Section 8 valuation table)

| Metric | Current | 5Y Avg | 5Y Med | 10Y Avg | 10Y Med | %-ile | Verdict |
|---|---|---|---|---|---|---|---|
| P/E TTM (GAAP) | ~X | ~Y | ~Z | ~A | ~B | NN% | Comfort/Neutral/Danger |
| Forward P/E | ~X | n/a | n/a | n/a | n/a | — | — |
| P/B | ~X | ~Y | ~Z | ~A | ~B | NN% | — |
| P/S | ~X | ~Y | ~Z | ~A | ~B | NN% | — |
| EV/EBITDA | ~X | ~Y | ~Z | ~A | ~B | NN% | — |
| FCF yield | ~X% | ~Y% | ~Z% | ~A% | ~B% | — | — |

Always cite source + flag MEDQ/LOWQ for averages.
