# Analyst Research — Tổng hợp quan điểm CTCK

> Pattern tổng hợp sell-side + independent analyst cho US stock. Đọc ở Phase 3 Section 20.

## A. Consensus data — aggregators

| Source | URL | Data |
|---|---|---|
| **TipRanks** | `tipranks.com/stocks/{TICKER}/forecast` | Consensus rating, target distribution, analyst by analyst, 3M tally |
| **MarketBeat** | `marketbeat.com/stocks/NYSE:{TICKER}/forecast/` | Analyst count, consensus, recent upgrades/downgrades |
| **CNN Business** | `cnn.com/markets/stocks/{TICKER}` | Simpler consensus |
| **Investing.com** | `investing.com/equities/{company}-consensus-estimates` | Intl coverage |
| **Yahoo Finance** | `finance.yahoo.com/quote/{TICKER}/analysis` | EPS estimates, growth |

**Output**: Buy/Hold/Sell %, average/median/high/low 12M target, vs current price upside.

## B. ⚠️ Caveat: target STALE

**Critical**: consensus target là LAGGING indicator. Đặt khi giá ở level cũ, sau khi stock move lớn → target stale, mong đợi loạt cut/revisions.

**Case ORCL**: consensus $268 đặt khi giá $200-280; sau crash $140 (tuần tồi tệ nhất 2001) → target vẫn $268, upside "+91%" là artifact, không thật. Wave of cuts sẽ đến trong 1-2 tháng sau big move.

**Action**: 
- Report target với AS-OF date rõ
- Flag "target stale, expecting revisions"
- Tính "target vs current price" nhưng cave at lag

## C. Bull vs Bear synthesis

### Bull case (synthesize từ sell-side bulls + independent)
- Top 5-7 bull arguments từ analyst notes + press + independent research
- Cite specific analyst (firm + name + date) khi quote
- Focus: KPI/growth/moat/margin expansion/re-rating catalyst

### Bear case (synthesize từ sell-side bears + rating agencies + skeptics)
- Top 5-8 bear arguments
- Cụ thể: capex sustainability, FCF, debt, counterparty, concentration, margin compression, regulatory, obsolescence, valuation
- Rating agencies (Fitch/S&P/Moody's) thường là honest bear voice — flag their concerns

### Independent view (non-sell-side, MEDQ but valuable)
- **SemiAnalysis** (Dylan Patel) — semis/AI infra deep dives
- **Stratechery** (Ben Thompson) — tech strategy
- **Deepwater Asset Management** (Gene Munster) — tech commentary
- **Substack ecosystem** — niche per industry
- **The Information** — tech internals
- **Seeking Alpha** — variable quality, crowd-sourced

## D. Specific analyst commentary — by firm (cover khi có thể)

For each major firm covering the stock, find LATEST: rating, target, thesis. Common firms:
- Morgan Stanley, Goldman Sachs, JP Morgan, Barclays, BofA, Citi, UBS, Jefferies, Wells Fargo, Stifel, Piper Sandler, Wedbush, Guggenheim, Bernstein, MoffettNathanson, Redburn, William Blair, D.A. Davidson, Oppenheimer, Roth MKM, Stephens

**For each**: report firm, analyst name (if found), date of latest note, rating (Strong Buy/Buy/Hold/Sell/Strong Sell or Outperform/Neutral/Underperform), price target, 1-2 sentence thesis summary. Direct quotes when available.

**Flag UNVERIFIED** khi:
- Analyst name không confirm
- Date không rõ
- Target có conflict giữa aggregators
- Coverage không rõ (firm có thực sự cover không)

## E. Recent catalysts & market reactions

- Last earnings (date, beat/miss, market reaction, analyst takeaways)
- Last 3 months rating changes (upgrades/downgrades table with date, firm, action)
- Major news moved stock (deal announcements, leadership, regulatory, etc.)

## F. Short interest & institutional flows

### Short interest
- **MarketBeat**: `marketbeat.com/stocks/NYSE:{TICKER}/short-interest/`
- **ShortSqueeze**: `shortsqueeze.com/shortinterest/stock/{TICKER}.htm`
- **S3 Partners**: institutional short data
- **FINRA**: bi-monthly short interest release (15th and end-of-month)

**Report**: shares short, % float short, days to cover, notional, trend (rising/falling).

**Interpret 2-way**: short interest cao = bearish bet NHƯNG cũng fuel cho short squeeze nếu catalyst positive.

### Institutional ownership
- **MarketBeat**: `marketbeat.com/stocks/NYSE:{TICKER}/institutional-ownership/`
- **13F.info**: `13f.info/cusip/{cusip}/` — quarterly 13F filings
- **Fintel**, **WhaleWisdom**, **Trendlyne**

**Report**: % institutional, top 10 holders (Vanguard, BlackRock, State Street typically), insider ownership %, recent 13F delta (add/trim by major funds), any activist.

**Caveat Q-1 13F**: filings lag 45 days, don't show shorts or international. Flag.

## G. Output format (Section 20)

### 20.1 Consensus snapshot
| Metric | Value |
|---|---|
| Coverage | N-M analysts |
| Consensus | Buy/Hold/Sell |
| Avg target | $X (+Y% vs current) |
| High target | $X (firm) |
| Low target | $X |
| Short interest | N shares (~$X notional), trend |

### 20.2 Analyst table
| Firm | Analyst | Rating | Target | Thesis |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |

### 20.3 Bull case (5-7 points with citations)
### 20.4 Bear case (5-8 points with citations)
### 20.5 Independent views (table)
### 20.6 Recent catalysts
### 20.7 Short interest + institutional
### 20.8 Synthesis: "report này hỗ trợ bear/bull ở đâu, neutral hơn analyst ở đâu"

## H. Anti-pattern

- ❌ Báo "consensus Buy + upside +91%" mà không flag target stale
- ❌ Quote analyst mà không cite source/date
- ❌ Only bulls (cheerlead) hoặc only bears (doom) — phải đối chiếu
- ❌ Confuse sell-side (biased bullish) với independent (more honest)
