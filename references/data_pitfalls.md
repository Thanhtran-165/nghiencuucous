# Data Pitfalls — 7 bẫy data cổ phiếu Mỹ

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

## Anti-pattern

- ❌ Lấy 1 số từ 1 nguồn không cross-check
- ❌ Report net income mà không flag "(derived)"
- ❌ Dùng non-GAAP "underlying" như main metric mà không flag SBC add-back
- ❌ Lộn FY với CY trong YoY comparison
