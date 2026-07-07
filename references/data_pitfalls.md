# Data Pitfalls — 9 bẫy data cổ phiếu Mỹ

> 7 lỗi common khi research US stock. Áp dụng ở Phase 1, cross-check mọi số liệu quan trọng. Đọc SKILL.md Lessons Learned #3, #4, #5, #10, #11 cho case studies.

## Bẫy 1: GAAP vs non-GAAP gap

**Vấn đề**: Công ty Mỹ thường report cả GAAP và non-GAAP ("adjusted") financials. Gap có thể lớn (case ORCL: FY26 GAAP EPS $5.83 vs non-GAAP $7.63 — gap 31%).

**Cause**: non-GAAP loại trừ stock-based compensation (SBC), amortization of acquired intangibles, restructuring charges, một lần items.

**Cách xử lý**:
- **P/E ratio**: SPECIFY GAAP hay non-GAAP. Default: GAAP (chặt). Forward P/E thường non-GAAP (guidance).
- **EPS**: report cả 2 nếu gap > 10%.
- **Operating margin**: GAAP truth, non-GAAP "underlying". Flag gap.
- **Caveat bull trap**: non-GAAP thường "loại trừ" SBC — nhưng SBC là real cost (pha loãng cổ đông). Buffett-style: luôn check GAAP.

## Bẫy 2: Fiscal year ≠ calendar year

**Vấn đề**: Mỗi công ty Mỹ có FY khác nhau. Lộn FY với CY = so sánh sai.

**Examples**:
- **AAPL**: FY kết thúc cuối September (FY2026 = 27/9/2026)
- **MSFT**: FY kết thúc 30/6 (FY2026 = 30/6/2026)
- **ORCL**: FY kết thúc 31/5 (FY2026 = 31/5/2026)
- **NVDA**: FY kết thúc cuối January (FY2027 = 1/2027)
- **COST**: FY kết thúc cuối August
- **WMT**: FY kết thúc 31/1
- **JPM, XOM, JNJ, KO, PG**: calendar year (31/12)

**Cách xử lý**:
- First mention: "FY2026 (kết thúc 31/5/2026)"
- Sortable table: dùng FY labels (FY24, FY25, FY26) không CY
- YoY comparison: cùng FY period (không lộn FY26 Q4 với CY2026 Q2)
- Macro context (recession, COVID): map FY → CY để đối chiếu

## Bẫy 3: Stock-based compensation (SBC) dilution

**Vấn đề**: Tech company phát hành stock rộng rãi cho employee. SBC là real economic cost (transfer from shareholders to employees) NHƯNG:
- GAAP: tính SBC trong operating expense (đúng)
- Non-GAAP: thường ADD-BACK SBC (sai — giả vờ SBC không phải cost)
- Diluted shares: tăng theo time do SBC vesting

**Case ORCL**: shares 2.78B → 2.91B FY26 = pha loãng từ SBC + equity raise.

**Cách xử lý**:
- Luôn check **diluted** shares (không basic)
- Track share count YoY — nếu tăng > 2%/năm mà không có M&A → dilution từ SBC
- Free Cash Flow: subtract SBC (FCF - SBC = "true FCF" cho shareholder). Nhiều aggregator không làm.
- Be skeptical của non-GAAP "FCF" không subtract SBC

## Bẫy 4: Adjusted vs reported (capitalized expenses)

**Vấn đề**: Một số công ty capitalize chi phí (đưa vào balance sheet thay vì expense) → inflate earnings ngắn hạn. Common với software development, content (Netflix), customer acquisition.

**Examples**:
- **NFLX**: capitalize content production → amortize qua time
- **SHOP**: historically capitalized software dev
- **PLUG/BLOOM**: capitalized equipment — Later impairment

**Cách xử lý**:
- Check "Capitalized software/content" line trên balance sheet
- Compare capex + capitalized expenses vs D&A
- Free Cash Flow truth = OCF - capex - capitalized expenses (nếu không đã include)

## Bẫy 5: Share class (A/B/C dual-class)

**Vấn đề**: Một số công ty có nhiều share class với voting rights khác nhau. Per-share metrics (EPS, BVPS) có thể khác nhau.

**Examples**:
- **GOOGL** (Class A, voting) vs **GOOG** (Class C, non-voting) — same economic rights, EPS same
- **BRK.A** vs **BRK.B** — 1500:1 ratio
- **META**: Class A (public) vs Class B (Zuckerberg control)
- **DIS**: previously dual-class
- **DISCA**/Warner: dual-class

**Cách xử lý**:
- Specify which ticker (GOOGL vs GOOG)
- For EPS/BVPS: dùng weighted-average diluted shares (combines all classes)
- Market cap: share count × current price (each class usually similar price)

## Bẫy 6: Net income derived vs reported

**Vấn đề**: Một số aggregator (Macrotrends, StockAnalysis) derive net income = EPS × shares thay vì lấy reported net income. Có thể chênh do rounding hoặc special items.

**Case ORCL**: FY26 net income ~$17B là DERIVED (EPS $5.83 × 2.91B shares), chưa confirm exact từ 10-K income statement.

**Cách xử lý**:
- Flag "(derived từ EPS)" nếu không có reported number
- Cross-check với 10-K income statement "Net income" line
- Discrepancy > 5%: flag, lấy 10-K为准

## Bẫy 7: Aggregator discrepancy (P/E, P/B, market cap)

**Vấn đề**: Nguồn khác nhau cho số khác nhau cho cùng metric.

**Case ORCL**:
- P/E TTM: Macrotrends 22×, Market Chameleon 24.4×, CNN 24.08× — range 22-24.4×
- P/B: Market Chameleon 10.9× vs my derivation 9.5× — chênh 15%
- Market cap: CNN ~$404B, tính tay = $140.27 × 2.91B = $408B — chênh 1%

**Cause**:
- Trailing twelve months (TTM) cutoff khác nhau
- Stock price as-of date khác
- Share count: diluted vs basic khác
- Book value: include/exclude goodwill, intangibles khác

**Cách xử lý**:
- Report **range + midpoint** thay vì 1 số duy nhất
- Cite ít nhất 2 nguồn cho mỗi metric quan trọng
- Flag là MEDQ (medium quality)
- Calculate tay từ primary data (price × shares = market cap) khi có thể

## Cross-check rule of thumb

| Metric | Tolerance | Action if outside |
|---|---|---|
| Revenue | < 1% | Check 10-K |
| Net income | < 3% | Check 10-K (derived?) |
| EPS diluted | exact | Phải match 10-K |
| OCF, FCF | < 5% | Check 10-K cash flow statement |
| P/E TTM | 2-5× | Multi-source range OK; flag |
| Market cap | 1-2% | Recompute = price × shares |
| Debt | 5-10% | "Long-term" vs "total borrowings" scope |

## Bẫy 8: Ngoại tệ / ADR (foreign listing)

**Vấn đề**: Công ty nước ngoài niêm yết ADR trên sàn Mỹ (NYSE/NASDAQ). Yahoo Finance trả price/market cap = USD, NHƯNG financials gốc trong 10-K/annual report = local currency (DKK, EUR, TWD, CNY, GBP).

**Examples**:
- **NVO** (Novo Nordisk, Đan Mạch): currency Yahoo = USD, NHƯNG 10-K gốc = DKK (tỷ giá ~7 DKK/USD)
- **TSM** (TSMC, Đài Loan): ADR, 10-K gốc = TWD
- **ASML** (Hà Lan): ADR, 10-K gốc = EUR
- **BABA** (Alibaba): ADR, 10-K gốc = CNY/RMB
- **SHEL, BP**: EUR/GBP

**Cách xử lý**:
- Phase 0 Step 0 preflight.py sẽ flag `FOREIGN_CURRENCY_OR_ADR` qua check `currency != USD` HOẶC `country != United States`
- **Verify financials gốc vs Yahoo**: lấy revenue từ 10-K gốc (local currency) + tỷ giá → compare với Yahoo number. Nếu lệch hệ số lớn (vd 7×) → Yahoo đã convert (OK) hoặc Yahoo sai (verify lại)
- **Label RÕ ở hero + mọi bảng**: "Doanh thu FY2026: 232B DKK (~$33B theo tỷ giá X/X/2026)"
- **Tỷ giá thay đổi**: nếu so sánh YoY, dùng cùng tỷ giá hoặc constant currency

## Bẫy 9: Lỗ / negative earnings (P/E vô nghĩa)

**Vấn đề**: Công ty đang trong giai đoạn tăng trưởng (growth company) hoặc suy thoái → EPS âm → **P/E TTM âm hoặc None → vô nghĩa**. Dùng P/E percentile / 3-zone verdict = misleading.

**Examples**:
- **SNOW** (Snowflake): EPS TTM -$3.51 → P/E = N/A (Yahoo None). Nếu skill tính P/E = price/(-3.51) = số âm → percentile sai hoàn toàn.
- **PLTR** (Palantir): gần hòa vốn, có kỳ lỗ có kỳ lãi → P/E volatile vô nghĩa
- **UBER, LYFT, RIVN, LCID, DDOG, NET, MDB, CRWD** (growth) — lỗ nhiều năm

**Cách xử lý**:
- Phase 0 Step 0 preflight.py sẽ flag `NEGATIVE_EARNINGS`
- **Path B (Valuation cho growth)**: dùng thay thế P/E:
  - **EV/Revenue** (Enterprise Value / Sales) — phổ biến nhất cho SaaS
  - **EV/Gross Profit** — khi margin chưa optimal
  - **Rule of 40** = growth rate % + margin % (vd 40% growth + 0% margin = 40 — passed)
  - **P/S** (Price/Sales) — đơn giản hơn EV/Revenue
  - **PEG dựa forward EPS** — nếu dự phóng lãi trong 1-2 năm
- **Flag RÕ**: "Công ty đang tăng trưởng, P/E không áp dụng. Dùng EV/Revenue + Rule of 40."
- **KHÔNG** tính P/E percentile cho công ty lỗ — chỉ confuse

## Anti-pattern

## Bẫy 10 (v2.2.4 — học từ CTD test VN): Báo cáo thiếu biểu đồ — visual gap

**Dấu hiệu:** Báo cáo HTML có data tables NHƯNG không charts.

**Cách phòng tránh:**
1. Dashboard PHẢI có tối thiểu 10 charts (Revenue/LNST, capex/FCF, segment mix, P/E history, peer scatter, price+MA, RSI, drawdown, distribution, valuation summary)
2. Verify `grep -c 'new Chart'` ≥ 10 trước deploy
3. Chart data phải thật từ yfinance, không simulate

**Rule:** Charts = phần visible nhất. Báo cáo không charts = thiếu chuyên nghiệp.
