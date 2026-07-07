---
name: us-equity-research
description: "Phân tích equity research đầy đủ cho cổ phiếu Mỹ (NYSE/NASDAQ) — pipeline 7 phase: data research → fundamental → valuation → dynamic insight engine → technical → analyst synthesis → dashboard HTML + deploy Vercel. Use when user gõ /us-equity-research [TICKER] hoặc yêu cầu 'phân tích', 'research', 'báo cáo', 'nghiên cứu' cho mã CP Mỹ cụ thể (AAPL, MSFT, NVDA, GOOGL, AMZN, META, TSLA, JPM, BRK, V, JNJ, XOM, COST...). Đặc trưng = INSIGHT ENGINE tạo 1-4 'Special Insight' sections TÙY THEO doanh nghiệp (không cố định) qua archetype router + câu hỏi gợi ý tương tác với user. Cốt lõi = clone pipeline đã chứng minh với báo cáo ORCL (22 sections, 70+ sources, deploy Vercel), output = dashboard HTML single-file + Vercel URL."
---

# /us-equity-research [TICKER]

Slash command chạy pipeline nghiên cứu cổ phiếu Mỹ đầy đủ — clone quy trình đã chứng minh với báo cáo Oracle (ORCL): 22 sections, citation bắt buộc, insight engine động, dashboard HTML deploy Vercel.

## Cách dùng

```
/us-equity-research NVDA           # Phân tích đầy đủ NVIDIA
/us-equity-research AAPL           # Phân tích đầy đủ Apple
/us-equity-research MSFT --fundamental-only   # Bỏ technical + analyst + deploy
/us-equity-research TSLA --insights 2         # Override số insight frames (default auto)
/us-equity-research JPM --capital 50000       # Vốn đầu tư tham chiếu $50K (default $33K)
/us-equity-research COST --period 5y          # Kỳ phân tích 5 năm (default 10y)
```

`[TICKER]` = mã cổ phiếu NYSE/NASDAQ (AAPL, MSFT, NVDA, GOOGL, AMZN, META, TSLA, JPM, BRK, V, JNJ, XOM, COST, PLD...)

## ⭐ Đặc trưng cốt lõi: INSIGHT ENGINE động

Khác với báo cáo cố định, skill này **KHÔNG có "special insight" hardcoded**. Thay vào đó:

1. **Phase 0 Discovery**: auto-detect sector (GICS) + archetype từ research ban đầu
2. **Archetype router**: đọc `references/insight_frames.md` → propose 2-4 insight frames từ thư viện 8 frames (value-chain positioning, margin defensibility, contract/backlog moat, counterparty risk, regulatory moat, cyclicality analog, capital allocation, ecosystem moat)
3. **Tương tác user**: user confirm / add / remove / edit frames → có thể thêm câu hỏi tự do ngoài thư viện
4. **Phase 2 Insight generation**: mỗi frame stress-test với data thật, **BẮT BUỘC** 1 "honest correction" callout (không cheerlead)

Đây là phần làm báo cáo ĐỘC ĐÁO theo từng doanh nghiệp — đúng yêu cầu "insight tùy doanh nghiệp".

## Pipeline 7 phase

> **Modularity note**: mỗi phase có entry/exit checkpoint rõ. Nếu 1 phase fail → báo lỗi rõ, KHÔNG tự bỏ qua. Hỏi user có continue với partial data không. Có thể chạy lại từng phase riêng (vd chỉ Phase 5 render nếu data đã có).

### Phase 0: Discovery (interactive — BẮT BUỘC trước khi fetch data)

**HARD GATE**: KHÔNG fetch data / viết report cho đến khi scope + insight frames được user confirm.

**Entry checkpoint**: user gõ `/us-equity-research [TICKER]` với optional flags.
**Exit checkpoint**: brief document chứa (ticker, period, capital, deploy?, technical?, analyst?, sector GICS, archetype, frames confirmed). User phải OK brief trước Phase 1.

#### Step 0: PREFLIGHT CHECK (mới — chống silent failure)

Chạy **trước** khi hỏi scope:
```bash
python3 scripts/preflight.py [TICKER] --period [10|5]
```

Trả JSON có `flags[]` + `go_no_go`. Xử lý theo `go_no_go`:

| go_no_go | Ý nghĩa | Action |
|---|---|---|
| **GO** | Không flag nguy hiểm | Chạy tiếp Step 1 bình thường |
| **WARN** | 1-2 flag (công ty lỗ / ADR / history thiếu / ticker đặc biệt) | Present flags cho user → chọn path → Step 1 |
| **STOP** | ≥3 flag nguy hiểm | Dừng, báo user, hỏi có continue không |

**Các flag quan trọng + path xử lý:**

| Flag | Path đề xuất |
|---|---|
| `NEGATIVE_EARNINGS` (EPS âm) | Valuation = path B: EV/Revenue + EV/Gross Profit + Rule of 40 thay P/E. Khai báo rõ "P/E không áp dụng". |
| `FOREIGN_CURRENCY_OR_ADR` (NVO, TSM, ASML, BABA) | Verify financials gốc vs Yahoo. Label currency RÕ ở hero + mọi bảng. Đừng mặc định USD. |
| `HISTORY_TOO_SHORT` (IPO < period) | Đề xuất giảm period. Flag "history limited to Xy" trong báo cáo. |
| `TICKER_HAS_SPECIAL_CHAR` (BRK.B, BF.B) | Folder name = sanitize (brk-b-deploy). Ticker yfinance giữ nguyên. |
| `ILLIQUID_SMALL_CAP` (< $100M) | Flag rõ. Cân nhắc bỏ technical PROFILE (data không đủ). |
| `YFINANCE_DATA_MISSING` (critical field thiếu) | Verify qua SEC EDGAR trước. Có thể Yahoo đổi API. |

**Đây là kỹ thuật "blindspot pass"** — áp dụng tinh thần bài Thariq: surface unknown unknowns TRƯỚC khi build, không phải sau khi báo cáo vỡ.

#### Step 1: Hỏi/confirm scope (chỉ SAU preflight OK)

1. Hỏi/confirm (1 câu/lần, multi-choice khi có thể):
   - Ticker + tên công ty (verify exchange NYSE/NASDAQ)
   - Kỳ phân tích: 5y hay 10y (default 10y — hoặc theo preflight recommendation nếu IPO ngắn)
   - Vốn đầu tư tham chiếu: **HỎI USER** (KHÔNG default $33,000 — mỗi nhà đầu tư có vốn khác nhau. Nếu user không trả lời → placeholder [VỐN_CỦA_BẠN])
   - Deploy Vercel hay chỉ local? (default deploy)
   - Có chạy technical (ACTIVE + PROFILE) không? (default có — nhưng nếu ILLIQUID_SMALL_CAP → đề xuất bỏ)
   - Có chạy analyst synthesis không? (default có)

#### Step 2: Quick research ban đầu

Subagent (~2 phút): WebSearch tên công ty + sector GICS + "business model" → xác định archetype.

#### Step 3: Archetype routing

Đọc `references/insight_frames.md` section "Archetype router" → propose 2-4 insight frames default cho sector đó. Present cho user:
- "Sector X (GICS) → default frames: [frame A, frame B, frame C]. Bạn muốn giữ, thêm, bớt, hay tự đặt câu hỏi riêng?"
- User confirm/edit → ghi vào brief document.

#### Step 4: Output Phase 0

Brief document: scope + capital + period + deploy? + insight frames confirmed + **preflight flags** (ghi rõ nếu có WARN).

### Phase 1: Data research (subagent song song — 4 streams)

**Entry checkpoint**: Phase 0 brief approved.
**Exit checkpoint**: structured JSON per stream, multi-source cross-checked, pitfalls applied.

**Primary: yfinance script** (`scripts/fetch_us_data.py`) — chạy trước cho structured data (price, financials, ratios, analyst targets, ~3 giây). Lấy 13 sections.

**Secondary: WebFetch subagent song song** — bổ sung qualitative (filings text, analyst commentary, news). Chạy **4 subagent song song** (read-only research, không viết file):

| Stream | Nguồn | Output |
|---|---|---|
| **(a) Filings** | SEC EDGAR (10-K, 10-Q, 8-K latest), company IR earnings release | FY financials: revenue, segment, OCF, capex, FCF, debt, cash, shares, RPO/backlog, dividend, buyback, **risk factors text, MD&A, commitments footnote** |
| **(b) Price data** | (yfinance đã lấy — verify cross-check Yahoo Finance API nếu cần) | OHLCV weekly 52w + daily ~500d, 52w high/low, current price, market cap |
| **(c) Fundamentals 10 năm** | (yfinance đã lấy annual statements — bổ sung Macrotrends/StockAnalysis nếu cần longer history) | Revenue, op income, net income, EPS diluted, OCF, capex, FCF, debt, diluted shares — 10 năm (hoặc 5 năm nếu `--period 5y`) |
| **(d) Analyst + news** | TipRanks/MarketBeat (consensus + targets), WSJ/Reuters/FT/CNBC/Bloomberg (deal news), SemiAnalysis/Stratechery (independent), Fitch/S&P/Moody's (credit) | Consensus rating, avg/high/low target, bull points, bear points, recent catalysts, short interest, institutional ownership |

**Áp dụng `references/data_pitfalls.md`**: 9 bẫy data US (GAAP vs non-GAAP, fiscal year, SBC dilution, adjusted vs reported, share class A/B/C, net income derived vs reported, aggregator discrepancy, **ngoại tệ/ADR, lỗ/negative earnings**). Cross-check multi-source cho số liệu quan trọng.

**Output Phase 1**: structured JSON per stream. Flag mọi số NOT FOUND / NOT VERIFIED — KHÔNG bịa.

### Phase 2: Insight engine (dynamic — phần ĐỘC ĐÁO)

Với **mỗi frame đã confirm ở Phase 0**, đọc template từ `references/insight_frames.md` → stress-test với data Phase 1.

**Mỗi insight section BẮT BUỘC cấu trúc:**
1. Trigger question (từ brief hoặc user-edited)
2. Analysis với data thật (citation footnote)
3. **"Honest correction" callout** — 1 luận điểm challenge bull reading đơn giản (VD ORCL: "rent nằm upstream không phải Oracle", "biên thấp là depreciation artifact", "$40B là pass-through")
4. Verdict + confidence level (high/medium/low)
5. KPI watchlist 3-5 điểm để biết thesis đúng/sai trong 3-5 năm
6. "Reframe cho nhà đầu tư X-K USD" closer

**Output Phase 2**: 1-4 Special Insight sections (số lượng + chủ đề động theo frames).

### Phase 3: 19 generic sections (skeleton cố định)

Viết content cho 19 section generic (theo `references/dashboard_design.md` section map):

| # | Section | Priority reference |
|---|---|---|
| 1 | Hero + KPI strip (6 KPI từ data) | — |
| 2 | Executive Summary (4 callouts: thesis/risk/valuation/X-K lens) + 💡 "Nói cách khác" | — |
| 3 | Business 101 — how makes money, segments, recurring vs one-time | — |
| 4 | Industry Position (3 layers) | — |
| 5 | Financial History 10 năm (bảng đầy đủ) | `references/valuation_formulas.md` |
| 6 | Segment Analysis (mix, growth, role) | — |
| 7 | Investment Thesis 3-5y + conditions right/wrong + KPI | — |
| 8 | Valuation — P/E P/B current vs 5Y/10Y avg/median + 3-zone verdict | `references/valuation_formulas.md` |
| 9 | Peer Comparison (5-7 peers, scatter chart) | — |
| 10 | Balance Sheet, Capex & FCF | — |
| 11 | Risk Matrix (14 risks × prob × impact × evidence × KPI) | — |
| 12 | X-K USD lens (lump-sum vs DCA, drawdown, checklist) | — |
| 13 | Scenario Analysis (Bull/Base/Bear) | — |
| 14 | Final Investment Checklist (Business/Financial/Valuation/Risk/Discipline) | — |
| 15-17 | **[DYNAMIC — từ Phase 2]** 1-4 Special Insight sections | `references/insight_frames.md` |
| 18 | Technical — Mode ACTIVE (Tech Score, Verdict) | `references/technical_methodology.md` |
| 19 | Technical — Mode PROFILE (NON-ADVICE) | `references/technical_methodology.md` |
| 20 | Analyst Synthesis (bull/bear, consensus target) | `references/analyst_research.md` |
| 21 | Glossary (financial generic + domain per company) | `references/language_layers.md` |
| 22 | Source Appendix + Data Quality (HIGHQ/MEDQ/LOWQ) | — |

### Phase 4: Language layers (readable cho retail)

Áp dụng 3-layer từ `references/language_layers.md`:
1. **Glossary** (section 21): financial generic (12 term cố định) + domain per company (12 term động)
2. **💡 "Nói cách khác" callouts**: ở Exec Summary + Valuation verdict + mỗi Insight conclusion + Moat conclusion
3. **Jargon kept**: tên riêng/chữ viết tắt chuẩn (EPS, P/E, GPU, NVIDIA, MACD...) giữ nguyên, footnote khi cần

### Phase 5: Dashboard render

1. Copy `assets/dashboard_template.html` → output folder `[TICKER_lowercase]-deploy/index.html`
2. **Token replace** qua `str.replace` (KHÔNG f-string — JS `{}` vỡ). Tokens: `{{TICKER}}`, `{{COMPANY_NAME}}`, `{{COMPANY_SUB}}`, `{{PRICE}}`, `{{PRICE_DATE}}`, `{{MARKET_CAP}}`, `{{KPI_STRIP}}`, `{{HISTORY_DATA}}`, `{{PEER_DATA}}`, `{{INSIGHT_SECTIONS}}`, `{{GLOSSARY_DOMAIN}}`, `{{REFS_LIST}}`, `{{DATA_QUALITY_MATRIX}}`, `{{CAPITAL_AMOUNT}}`, etc.
3. **Tự động generate TOC + xref link** (pattern Python đã dùng cho ORCL): scan section ids → build TOC grid; convert "Section N" text → `<a href="#sec-..." class="xref">`
4. **Verify**:
   - `node --check` trên inline JS (extract `<script>` ra tempfile)
   - `grep -oE "\{\{[A-Z_0-9]+\}\}"` phải rỗng (không sót token)
   - `grep -iE "bullish\|bearish\|khuyến nghị mua\|khuyến nghị bán\|strong buy\|strong sell\|tín hiệu vào\|tín hiệu ra"` trong PROFILE section (18/19) phải rỗng — **BẮT BUỘC non-advice**
   - Mở browser smoke test (optional, nếu Playwright available)

### Phase 6: Quality gates + deploy

**⚠️ CHẤT LƯỢNG > TỐC ĐỘ** (v2.2.5 — học từ CTD test VN 7/2026)

> **Nguyên tắc tối thượng**: KHÔNG ưu tiên "xong nhanh". Ưu tiên "đúng spec + đủ chất lượng".
> Một báo cáo thiếu charts/citations/depth nhưng deploy nhanh = **thất bại**, không phải thành công.

**Rule 1: Đọc lại reference files TRƯỚC mỗi phase**

KHÔNG build theo "nhớ đại khái". Trước mỗi phase, **mở và đọc** reference file liên quan:

| Phase | Reference BẮT BUỘC đọc trước khi build |
|---|---|
| Phase 0 Discovery | `insight_frames.md` Section A (archetype router) + Section I (đặc thù ngành) |
| Phase 1 Data | `data_pitfalls.md` (10 bẫy) + `data_sources.md` |
| Phase 3 Sections | `insight_frames.md` Section B-I + `analyst_research.md` + `valuation_formulas.md` |
| Phase 5 Render | `dashboard_design.md` (22 section map + chart recipes) + benchmark report (ORCL/NEM) |
| Phase 6 Deploy | **Quality Gate checklist bên dưới** |

**Rule 2: Quality Gate BẮT BUỘC trước deploy — KHÔNG SKIP**

```bash
# Chạy TẤT CẢ checks. Nếu bất kỳ FAIL → BLOCK deploy, fix trước.

# 1. Charts minimum (Bẫy 9/10)
CHART_COUNT=$(grep -c 'new Chart\|viz.chart' [output].html)
[ "$CHART_COUNT" -ge 10 ] || echo "❌ FAIL: chỉ $CHART_COUNT charts (minimum 10)"

# 2. Citations minimum
REF_COUNT=$(grep -oE 'class="ref"' [output].html | wc -l)
[ "$REF_COUNT" -ge 10 ] || echo "❌ FAIL: chỉ $REF_COUNT citations (minimum 10)"

# 3. Sections count
SEC_COUNT=$(grep -c '<section' [output].html)
[ "$SEC_COUNT" -ge 20 ] || echo "❌ FAIL: chỉ $SEC_COUNT sections (minimum 20)"

# 4. Callout "Nói cách khác" minimum (3-layer language)
CALLOUT_COUNT=$(grep -c 'Nói cách khác' [output].html)
[ "$CALLOUT_COUNT" -ge 5 ] || echo "❌ FAIL: chỉ $CALLOUT_COUNT callouts (minimum 5)"

# 5. Honest corrections (mỗi insight phải có)
HONEST_COUNT=$(grep -c 'HONEST CORRECTION\|honest correction' [output].html)
[ "$HONEST_COUNT" -ge 3 ] || echo "❌ FAIL: chỉ $HONEST_COUNT honest corrections (minimum 3)"

# 6. Data Quality Matrix rows
DQ_ROWS=$(sed -n '/Data Quality/,/<\/table>/p' [output].html | grep -c '<tr')
[ "$DQ_ROWS" -ge 10 ] || echo "❌ FAIL: chỉ $DQ_ROWS DQ rows (minimum 10)"

# 7. Source Appendix có numbered citations
SOURCE_REFS=$(grep -oE 'id="ref-[0-9]+"' [output].html | wc -l)
[ "$SOURCE_REFS" -ge 10 ] || echo "❌ FAIL: chỉ $SOURCE_REFS numbered sources (minimum 10)"

# 8. Placeholder tokens empty
TOKENS=$(grep -oE '\{\{[A-Z_0-9]+\}\}' [output].html | wc -l)
[ "$TOKENS" -eq 0 ] || echo "❌ FAIL: $TOKENS unreplaced tokens"

# 9. Non-advice PROFILE check
PROFILE_ADVICE=$(sed -n '/sec-tech-profile/,/sec-analyst/p' [output].html | grep -ciE 'bullish|bearish|khuyến nghị mua|khuyến nghị bán|strong buy|strong sell')
[ "$PROFILE_ADVICE" -eq 0 ] || echo "❌ FAIL: PROFILE has advice language"

# 10. Div balance
OPENS=$(grep -oE '<div[ >]' [output].html | wc -l)
CLOSES=$(grep -oE '</div>' [output].html | wc -l)
[ "$OPENS" -eq "$CLOSES" ] || echo "❌ FAIL: div imbalance $OPENS/$CLOSES"

# 11. GAAP vs non-GAAP flagged
GAAP_FLAG=$(grep -ciE 'GAAP|non-GAAP' [output].html)
[ "$GAAP_FLAG" -ge 2 ] || echo "❌ FAIL: GAAP/non-GAAP not specified"

# 12. Fiscal year flagged
FY_FLAG=$(grep -ciE 'FY[0-9]|fiscal year|kết thúc' [output].html)
[ "$FY_FLAG" -ge 1 ] || echo "❌ FAIL: fiscal year not flagged"
```

**Rule 3: Benchmark comparison BẮT BUỘC**

Trước deploy, **so sánh với benchmark report** (ORCL hoặc NEM):

| Metric | Benchmark (ORCL/NEM) | New report minimum | Nếu < minimum |
|---|---|---|---|
| Size | ~150-250KB | ≥ 120KB | BLOCK |
| Charts | 13 | ≥ 10 | BLOCK |
| Sections | 22 | ≥ 20 | BLOCK |
| Citations | 16-69 | ≥ 10 | BLOCK |
| Callouts | 7-8 | ≥ 5 | BLOCK |
| Data Quality rows | 13-14 | ≥ 10 | BLOCK |

**Nếu new report <80% benchmark ở bất kỳ metric nào → BLOCK deploy. Fix cho đủ rồi deploy.**

**Rule 4: KHÔNG "xong vội"**

- User không phản đối đợi thêm 10-15 phút nếu cần đạt quality
- Thà deploy chậm nhưng đúng spec, hơn deploy nhanh nhưng thiếu charts/citations/depth
- **"Hoàn thành" = pass ALL quality gates, KHÔNG phải "deploy xong"**

---

**Quality gates cũ (vẫn áp dụng):**
- [ ] 22 sections đầy đủ (hoặc 17-19 nếu `--no-technical`/`--no-analyst`)
- [ ] Mỗi số liệu lớn có footnote citation
- [ ] Insight sections có "honest correction" callout
- [ ] PROFILE section non-advice language verified
- [ ] GAAP vs non-GAAP specified khi dùng P/E
- [ ] Fiscal year vs calendar year flagged
- [ ] NOT FOUND / NOT VERIFIED marked honest (không bịa)
- [ ] KHÔNG có "khuyến nghị mua/bán" tuyệt đối, KHÔNG target price nếu không có model rõ

**Deploy** (nếu user confirm ở Phase 0):
```bash
mkdir -p ~/ZCodeProject/[ticker]-deploy
# write index.html vào đó
vercel deploy ~/ZCodeProject/[ticker]-deploy --prod -y   # timeout 600000ms
```

## Tùy chọn (flags)

| Flag | Ví dụ | Action |
|---|---|---|
| Bỏ technical + analyst + deploy | `/us-equity-research AAPL --fundamental-only` | Chỉ phase 1-4 + 15 sections (bỏ 18-20), không deploy |
| Bỏ technical | `/us-equity-research TSLA --no-technical` | Bỏ section 18-19 |
| Bỏ analyst | `/us-equity-research JPM --no-analyst` | Bỏ section 20 |
| Đổi số insight | `/us-equity-research NVDA --insights 2` | Override archetype default, chạy đúng 2 frames |
| Đổi vốn tham chiếu | `/us-equity-research MSFT --capital 100000` | Default $33,000 → $100,000 cho X-K lens section |
| Đổi kỳ phân tích | `/us-equity-research COST --period 5y` | 5 năm (default 10y) |
| Không deploy | `/us-equity-research XOM --no-deploy` | Chỉ tạo file local |

Nếu không có flag → chạy full pipeline mặc định (insight frames auto-propose, deploy Vercel).

## Output cuối cùng

1. **File `[TICKER]-deploy/index.html`** (dashboard 22 sections, single-file, ~150-250KB, Chart.js + glossary + TOC + xref)
2. **URL Vercel** (nếu deploy)
3. **Tóm tắt insight engine**: sector detected, archetype, frames đã chạy, "honest correction" cho mỗi frame
4. **Data quality summary**: HIGHQ/MEDQ/LOWQ breakdown, NOT FOUND items

## Nguyên tắc cốt lõi (áp dụng mọi phase)

- ✅ **Data THẬT** từ nguồn chính thức (SEC EDGAR, company IR, Yahoo Finance, Macrotrends, StockAnalysis)
- ✅ **Cross-check** multi-source cho số liệu quan trọng (LNST, EPS, FCF, debt, RPO)
- ✅ **Insight engine ĐỘNG**: frames từ archetype + user confirm, KHÔNG hardcoded
- ✅ **Honest correction BẮT BUỘC** trong mỗi insight frame — không cheerlead
- ✅ **PROFILE section non-advice** (grep verify — không "bullish/bearish/khuyến nghị")
- ✅ **Citation footnote** cho mỗi số liệu quan trọng
- ✅ **3-layer language**: glossary + 💡 Nói cách khác + jargon kept
- ❌ **KHÔNG bịa** số liệu, KHÔNG mô phỏng data giá
- ❌ **KHÔNG claim** pattern/divergence nếu data không show
- ❌ **KHÔNG khuyến nghị** mua/bán tuyệt đối
- ❌ **KHÔNG target price** nếu không có model DCF rõ ràng
- ❌ **KHÔNG dùng** f-string Python với JS (brace vỡ) — dùng `str.replace`

## ⚠️ Lessons learned (từ case ORCL 2026 + best practice)

1. **Phase 0 Discovery BẮT BUỘC** — không skip. Insight frames sai = báo cáo generic, mất giá trị. Case ORCL: 3 frames (value-chain, barriers, supply) chỉ đúng vì user hỏi đúng câu.

2. **Archetype router không hoàn hảo** — Conglomerate (BRK), công ty đa ngành, sector mới → user override. Skill đề xuất default nhưng KHÔNG ép.

3. **GAAP vs non-GAAP gap lớn** — Case ORCL: FY26 GAAP $5.83 vs non-GAAP $7.63 (gap 31%). Phải specify khi dùng P/E; forward P/E thường non-GAAP guidance.

4. **Fiscal year ≠ calendar year** — ORCL FY kết thúc 31/5, MSFT 30/6, AAPL cuối tháng 9, NVDA cuối tháng 1. Flag rõ "FY2026 (kết thúc 31/5/2026)".

5. **RPO/backlog ≠ revenue ngay** — Case ORCL: $638B RPO nhưng ~$75B là customer-supplied GPUs/prepayment (kinh tế khác cloud thường). Phải phân tích quality conversion.

6. **Token replace `str.replace`, KHÔNG f-string** — JS có `{}` (object literals, Chart config) sẽ vỡ với Python f-string. Pattern: define TOKEN_MAP dict → loop replace. Verify `grep -oE "\{\{[A-Z_0-9]+\}\}"` rỗng sau fill.

7. **PROFILE non-advice grep BẮT BUỘC** — Case ORCL đã mắc: lỡ trộn ngôn ngữ "bullish" vào PROFILE. Fix: `grep -iE "bullish|bearish|khuyến nghị mua|khuyến nghị bán"` trong section PROFILE phải rỗng.

8. **"Honest correction" là differentiator** — Case ORCL: 3 insight đều có correction (rent upstream, depreciation artifact, pass-through). Đây là phần làm báo cáo KHÁC với cheerleading sell-side note. BẮT BUỘC mỗi frame.

9. **TOC + xref tự động** — Báo cáo dài 22 section cần điều hướng. Pattern Python đã chứng minh: scan section ids → TOC grid; regex "Section N" trong text chunks (không tag) → `<a class="xref">`.

10. **Multi-source discrepancy flag** — Case ORCL: P/E range 22-24.4×, P/B 9.5-10.9× giữa Macrotrends/Market Chameleon/CNN. Báo cáo dùng midpoint + flag, không bịa 1 số duy nhất.

11. **Analyst target STALE** — Case ORCL: consensus $268 đặt khi giá $200-280; sau crash $140 → target stale, mong đợi cut. Flag rõ "target đặt lúc nào, giá hiện tại bao nhiêu".

12. **Counterparty risk underweighted** — Case ORCL: OpenAI loss ~$20.9B/năm, Oracle raise vốn ngoài finance capex cho OpenAI. Đây là concentration risk thật, phải phân tích honest.

13. **Preflight check BẮT BUỘC** (mới, sau bài Thariq 7/2026) — Chạy `scripts/preflight.py` ở Phase 0 Step 0 TRƯỚC khi hỏi scope. Surface 3 silent-failure cases: (a) công ty lỗ → P/E vô nghĩa, (b) ADR/ngoại tệ → lẫn đơn vị, (c) IPO ngắn → history thiếu. Không chạy preflight = chưa biết skill có vỡ không trước khi build. Case test: SNOW (EPS -$3.51 → WARN), NVO (ADR Đan Mạch → WARN), BRK.B (ticker dấu chấm → folder sanitize).

14. **ADR detection phức tạp hơn nghĩ** — Yahoo field `currency` có thể đã convert ADR sang USD (case NVO: currency=USD nhưng country=Denmark). Phải check CẢ currency + country. Financials gốc trong 10-K vẫn là local currency (DKK/EUR/TWD). Verify Yahoo number vs 10-K — nếu lệch hệ số lớn = sai tỷ giá.

15. **Đặc thù ngành BẮT BUỘC — đọc số tài chính đúng cách** (học từ CTD test VN 7/2026, port sang US) — Đọc số tài chính mà không hiểu bản chất ngành = **bias chắc chắn**. Mỗi ngành có "lens" riêng (Software: ARR/NRR/SBC; Mining: AISC/P/NAV; REITs: P/FFO/WALE; Banks: P/B/NIM/CET1). Phân tích không đọc `references/insight_frames.md` Section I trước = số liệu đúng nhưng kết luận sai. Rule: **hỏi user "đặc thù ngành X là gì?" + WebSearch pitfalls + tạo bảng đặc thù trước khi analyze.**

## Tham khảo (progressive disclosure)

SKILL.md giữ lean (<500 dòng). Detail nặng đọc reference khi cần:

| File | Khi nào đọc | Priority |
|---|---|---|
| `references/insight_frames.md` | **Phase 0 + 2** (BẮT BUỘC) — 8 frames + archetype router | ⭐⭐⭐ CORE |
| `references/data_sources.md` | Phase 1 — 10 source categories + URL pattern + fallback | ⭐⭐ |
| `references/data_pitfalls.md` | Phase 1 — 9 bẫy data US | ⭐⭐ |
| `references/valuation_formulas.md` | Phase 3 section 5+8 — P/E P/B avg/median, DCF, percentile | ⭐⭐ |
| `references/technical_methodology.md` | Phase 3 section 18-19 — ACTIVE + PROFILE (Yahoo data) | ⭐⭐ |
| `references/analyst_research.md` | Phase 3 section 20 — bull/bear synthesis pattern | ⭐ |
| `references/language_layers.md` | Phase 4 — glossary template + 💡 callout pattern | ⭐ |
| `references/dashboard_design.md` | Phase 5 — 22 section map, CSS, Chart.js wiring, TOC/xref pattern | ⭐⭐ |
| `assets/README.md` | Phase 5 — cách dùng assets (skeleton + example) | ⭐⭐ |
| `assets/dashboard_skeleton.html` | Phase 5 — **⭐ WORKING TEMPLATE primary** (54KB, 105 tokens, clean) | ⭐⭐⭐ CORE |
| `assets/dashboard_example_orcl.html` | Phase 5 — **reference example** ORCL hoàn chỉnh (depth benchmark) | ⭐⭐⭐ CORE |
| `assets/dashboard_template.html` | (legacy) ORCL report tokenized — superseded by skeleton | ⭐ |
| `scripts/fetch_us_data.py` | Phase 1 — **⭐ PRIMARY data fetcher** (yfinance, 13 sections, 3 giây) | ⭐⭐⭐ CORE |
| `scripts/preflight.py` | **Phase 0 Step 0** — kiểm tra công ty lỗ / ADR / IPO ngắn / ticker đặc biệt TRƯỚC khi build | ⭐⭐⭐ CORE (chống silent failure) |

## Lưu ý thực thi

- Pipeline mất **15-40 phút** tùy ticker (4 subagent research song song + insight engine + render + deploy)
- **WebFetch-based**: một số source (WSJ, FT) có thể paywall → flag và dùng fallback (Reuters, CNBC, Bloomberg free tier)
- **Yahoo Finance Chart API**: `query2.finance.yahoo.com/v8/finance/chart/{TICKER}?range={1y|2y}&interval={1wk|1d}` — free, không key, CORS-friendly
- **Vercel deploy**: cần đã login (`vercel login`) 1 lần; CLI tại `/Users/bobo/.local/bin/vercel`, đã auth `thanhtran-165`
- Nếu 1 phase fail → báo lỗi rõ, KHÔNG tự bỏ qua hoặc fake data. Hỏi user có continue với partial data không.
