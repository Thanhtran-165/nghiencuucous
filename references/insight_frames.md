# Insight Frames — Thư viện 8 frame + Archetype Router

> ⭐ **CORE REFERENCE** — Đây là phần làm báo cáo ĐỘC ĐÁO theo từng doanh nghiệp. Đọc BẮT BUỘC ở Phase 0 (Discovery) + Phase 2 (Insight generation).

Skill **KHÔNG hardcoded** "special insight" (như AI value chain cho Oracle). Thay vào đó, mỗi báo cáo generate 1-4 insight sections **tùy doanh nghiệp** qua cơ chế:

1. **Archetype router** (sector GICS → default frames) — auto-propose
2. **User confirm/add/remove** — interactive Phase 0
3. **Frame stress-test với data thật** — Phase 2, mỗi frame BẮT BUỘC có "honest correction"

---

## A. Archetype Router (sector GICS → default frames)

Khi Phase 0 detect sector, propose default frames từ bảng dưới. **ĐÂY LÀ ĐỀ XUẤT, KHÔNG ÉP** — user có thể override.

| Sector (example tickers) | Default frames (auto-propose) | Sections ưu tiên | KPI đặc thù |
|---|---|---|---|
| **Tech / Semis** (NVDA, AAPL, AVGO, TSM, AMD, INTC, QCOM, MU) | 1 value-chain + 8 ecosystem + 7 capital alloc | R&D/rev, PEG, design win | Gross margin, R&D %, unit shipments |
| **Software / Cloud** (MSFT, ORCL, CRM, ADBE, NOW, INTU, SNOW) | 1 value-chain + 2 margin + 3 contract/backlog | ARR, NRR, FCF | NRR, ARR growth, FCF margin, RPO |
| **Internet / Consumer Tech** (GOOGL, META, AMZN, NFLX, UBER, BABA) | 8 ecosystem + 7 capital alloc | MAU/ARPU, ad rev, take rate | MAU, ARPU, ad revenue %, engagement |
| **Banks / Financial** (JPM, BAC, GS, MS, WFC, C, BLK) | 5 regulatory + 7 capital alloc + 4 counterparty | P/B, ROE, NIM, Tier-1 | NIM, ROE, Tier-1 capital, NPL %, efficiency |
| **Insurance** (BRK, UNH-insurance, AIG, MET) | 5 regulatory + 7 capital alloc + 6 cyclicality | Combined ratio, float | Combined ratio, float, investment yield |
| **Healthcare / Pharma** (JNJ, PFE, MRK, LLY, ABBV, UNH) | 5 regulatory + 8 ecosystem (patent moat) | Pipeline, P/E vs growth | Pipeline depth, patent cliff, R&D, FDA approvals |
| **Biotech** (MRNA, VRTX, REGN, GILD) | 5 regulatory + 6 cyclicality | Pipeline binary risk | Phase 3 trials, cash runway, binary outcomes |
| **Medical Devices / Tools** (MDT, SYK, ABT, TMO, ILMN) | 5 regulatory + 8 ecosystem | Razor-blade model | Installed base, consumable recurring % |
| **Energy / Oil & Gas** (XOM, CVX, COP, SLB, EOG, PXD) | 6 cyclicality + 7 capital alloc | EV/EBITDA, P/CF, reserve | Reserve life, production growth, FCF, commodity price |
| **Utilities** (NEE, DUK, SO, AEP) | 5 regulatory + 7 capital alloc | Dividend yield, P/E | Rate base growth, ROE allowed, dividend payout |
| **REITs** (PLD, AMT, O, SPG, CCI, EQIX) | 7 capital alloc + 5 regulatory | P/FFO, NAV, occupancy | FFO/share, occupancy, WALE, cap rate |
| **Consumer / Retail / Staples** (COST, WMT, PG, KO, PEP, CL) | 8 ecosystem (brand/distribution) + 7 capital alloc | SSSG, gross margin, inventory | SSSG, gross margin, inventory turns, brand share |
| **Consumer Discretionary** (HD, LOW, NKE, SBUX, TGT) | 8 ecosystem + 6 cyclicality | SSSG, traffic vs ticket | SSSG, traffic, AUV, store count |
| **EV / Auto / Industrial** (TSLA, GM, F, GE, HON, CAT) | 1 value-chain + 6 cyclicality + 2 margin | Production, margin, capex | Production volume, gross margin/unit, capex intensity |
| **Aerospace / Defense** (LMT, RTX, NOC, GD) | 5 regulatory + 3 contract/backlog | Backlog, program execution | Backlog/book-to-bill, program margin, defense budget |
| **Payments / Fintech** (V, MA, PYPL, SQ, AXP) | 8 ecosystem (network) + 5 regulatory + 7 capital alloc | Take rate, volume | GDV growth, take rate, cross-border volume |
| **Telecom** (T, VZ, TMUS) | 5 regulatory + 7 capital alloc + 8 ecosystem | ARPU, churn, coverage | Postpaid ARPU, churn, 5G coverage |
| **Conglomerate** (BRK, GE-pre) | **User override bắt buộc** — chọn sub-business focus | Varies | Look-through earnings, segment ROIC |

**Cách dùng bảng:**
1. Phase 0 research → xác định GICS sector + sub-industry
2. Tìm row match → lấy "Default frames"
3. Present cho user: *"Sector X → default propose frames [A, B, C]. Có giữ/thêm/bớt hay tự đặt câu hỏi riêng không?"*
4. User confirm/edit → ghi vào brief

**Edge cases:**
- **Conglomerate (BRK)**: KHÔNG auto-propose — hỏi user focus sub-business nào (insurance vs railroad vs energy vs equity portfolio)
- **Sector mới /không có trong bảng**: propose frames 7 (capital allocation) + 2 (margin defensibility) — 2 frame tổng quát nhất, rồi user add
- **Công ty chuyển mình** (vd TSLA từ auto → AI/robotics): dùng thesis keyword thay vì sector → frame 1 (value-chain) + 8 (ecosystem)

---

## B. 8 Insight Frames (thư viện skeleton)

Mỗi frame = template tái dùng. **BẮT BUỘC cấu trúc 6 phần** trong output (xem SKILL.md Phase 2).

### Frame 1 — Value-chain positioning ("có phải trụ cột không?")

**Trigger condition**: Công ty được pitched là 1 mắt xích trong chuỗi giá trị hot (AI infrastructure, EV battery, semiconductor, green energy, biotech tools...). User hoặc thesis claim công ty là "pillar"/"trụ cột"/"indispensable" của chuỗi đó.

**Trigger phrasing examples (để nhận diện câu hỏi user):**
- "Công ty X có phải trụ cột của ngành Y không?"
- "Liệu công ty X có hưởng lợi từ [trend] không?"
- "X có indispensable cho tương lai [trend] không?"

**Template structure (đổ data vào):**
1. **Bản đồ chuỗi giá trị** — vẽ 6-8 tầng từ upstream nhất (raw material/silicon) → downstream nhất (end application). Mỗi tầng: key players + bottleneck severity + margin/rent profile + indispensability rating.
2. **Vị trí công ty** — highlight tầng công ty ngồi. Owns/Buys/Rents các asset gì?
3. **"Ai ăn rent?" analysis** — sơ đồ phân bổ $1 revenue của end-product cho các tầng. Tầng nào margin cao nhất? Công ty ở tầng đó không?
4. **Verdict**: công ty có phải "trụ cột" không? (pillar / beneficiary / downstream aggregator / commodity layer)

**⚠️ HONEST CORRECTION (BẮT BUỘC):**
> "Trụ cột thật nằm ở đâu? Công ty [TICKER] thực sự ngồi ở tầng đó không?"
- Challenge claim "pillar" bằng cách chỉ ra tầng nào mới thật sự indispensable (thường là upstream — silicon/foundry/IP, không phải downstream assembler)
- Case ORCL: user claim "Oracle là trụ cột AI" → honest correction: "trụ cột thật là NVIDIA + TSMC + HBM; Oracle là downstream aggregator mua GPU"

**KPI watchlist (3-5 điểm):**
- Margin trajectory của công ty vs upstream supplier (nếu supplier GM > công ty GM → rent leak upstream)
- Market share công ty trong tầng đó (có durable không)
- Pricing power của công ty (có raise price được không)
- Upstream supplier concentration (1-2 supplier = risk)

---

### Frame 2 — Margin defensibility / Barriers to entry ("biên thấp nhưng có ai vào thay được không?")

**Trigger condition**: Công ty có biên thấp, hoặc capex-heavy thesis, hoặc user hỏi "biên thấp có thể raise được không", "barrier cao không", "có ai vào cạnh tranh không".

**Trigger phrasing:**
- "Biên thấp nhưng có ai thay được không?"
- "Rào cản gia nhập cao không?"
- "Có thể raise margin khi workload mature không?"

**Template structure:**
1. **Bảng 9 rào cản Porter + platform economics**:
   - (a) Capital intensity — min viable scale
   - (b) Supplier allocation (GPU/chip/license allocation)
   - (c) Site/power/land procurement
   - (d) Time-to-capacity
   - (e) Technical IP/fabric/engineering
   - (f) Enterprise trust/compliance/certifications
   - (g) Sales motion + enterprise relationships
   - (h) Software ecosystem depth
   - (i) Scale economics / unit cost
2. Mỗi rào cản: chiều cao (High/Med/Low) + xu hướng (Rising/Falling/Stable) + bảo vệ ai
3. **Switching cost matrix** — 5-6 tầng workload (data → inference → training → managed service → enterprise SaaS). Mỗi tầng: lock-in strength + direction (increasing/decreasing).
4. **Verdict**: defensible (incumbent protected) vs commodity (low barrier, margin compresses).

**⚠️ HONEST CORRECTION:**
> "Biên thấp có phải artifact depreciation timing không? Rào cản đang tăng hay giảm?"
- Phân biệt "margin thấp vĩnh viễn" (commodity) vs "margin thấp tạm thời" (capex ramp depreciation artifact). Case ORCL: 14-16% GM bao gồm depreciation trong COGS →Oracle guide 35% ở scale → correction hướng bull.
- Nhưng cũng flag: rào cản nào đang FALLING (vd GPU allocation khi supply catch up) — không phải mọi rào cản durable.

**KPI watchlist:**
- Margin trajectory (clean disclose nếu có)
- Market share trend (gaining/losing)
- New entrant count + their economics
- Pricing power ($/unit trend)

---

### Frame 3 — Contract / backlog-as-moat ("RPO/backlog có tạo fleet fungible không?")

**Trigger condition**: Backlog/RPO là KPI headline của công ty. User hoặc thesis claim "$X backlog = guaranteed revenue". Công ty aerospace/defense, cloud/SaaS với RPO lớn, EPC contractor...

**Trigger phrasing:**
- "Backlog $X = revenue đảm bảo không?"
- "Hợp đồng dài hạn có tạo moat không?"
- "RPO có convert thành cash flow không?"

**Template structure:**
1. **Phân biệt allocation vs long-term contract** — 2 cơ chế khác nhau:
   - Real-time allocation (quarterly supplier decision)
   - Long-term purchase commitment (multi-year binding, có prepayment)
2. **Counterparty-funded vs company-funded** — hợp đồng $X là:
   - Company owns the asset (fungible, real moat)?
   - Customer-funded pass-through (asset dedicated to 1 customer, no fleet value)?
3. **Conversion analysis**: backlog historical → revenue conversion rate; cancellation rate; renegotiation risk
4. **Ranking** — công ty vs peers: ai có contracted access mạnh nhất? (diversified vs concentrated)

**⚠️ HONEST CORRECTION:**
> "Hợp đồng có tạo fleet fungible không, hay pass-through cho 1 khách?"
- Case ORCL: "$40B NVIDIA deal" nghe như moat nhưng thực là customer-funded pass-through cho OpenAI (GPU dedicated, không fungible cho OCI). Contractual obligation, không phải asset.
- Flag: ai bear risk nếu customer default?

**KPI watchlist:**
- Backlog conversion rate historically
- Customer concentration in backlog (% top 1, top 5)
- Counterparty financials (loss-making? credit rating?)
- Purchase commitments footnote (10-K) — $ committed to suppliers, timeframe

---

### Frame 4 — Counterparty / customer-concentration risk

**Trigger condition**: 1 vài khách hàng lớn drive thesis. Công ty dependent on few customers (Apple suppliers, cloud dependent on 1 AI lab, defense prime với 1 program...).

**Trigger phrasing:**
- "Khách lớn có trả được nợ không?"
- "Concentration risk thế nào?"
- "Nếu khách X mất thì ảnh hưởng bao nhiêu?"

**Template structure:**
1. **Counterparty financials** — top 1-3 khách: revenue, profitability, cash flow, credit rating, funding situation
2. **Concentration %** — top 1 = X% revenue/backlog; top 5 = Y%. So với peer median.
3. **Default scenario** — nếu top 1 khách default/renegotiate/churn: revenue impact, balance sheet impact, recovery path
4. **Structural comparison** — diversified base (defensible) vs few bilateral deals (concentration risk)

**⚠️ HONEST CORRECTION:**
> "Khách lớn nhất có khả năng trả được không? Ai bear risk nếu default?"
- Case ORCL: OpenAI loss ~$20.9B/năm, profitability không trước 2029. Oracle raise vốn ngoài finance capex → concentration risk really.
- So sánh với peer (Microsoft diversified across thousands customers + OpenAI) — structure khác biệt.

**KPI watchlist:**
- Counterparty profitability trajectory
- Concentration % over time (gaining/losing)
- Default/recovery history trong industry
- Contractual risk allocation (10-K disclosure)

---

### Frame 5 — Regulatory / compliance moat

**Trigger condition**: Công ty trong regulated industry (healthcare, finance, banking, govtech, telecom, utilities, cannabis, gaming...). License/permit/certification là barrier.

**Trigger phrasing:**
- "License/regulatory có tạo moat không?"
- "Barrier compliance cao không?"
- "Regulatory risk thế nào?"

**Template structure:**
1. **License/permit matrix** — công ty có gì? (FDA, FedRAMP, banking charter, telecom license, gaming license, FCC...). Thời gian + cost để earn.
2. **Switching cost regulator-created** — khách khó đổi sang đối thủ vì compliance dependency (vd database trong regulated industry có audit trail requirement)
3. **Incumbent advantage** — early license holder có durable edge?
4. **Policy risk** — regulatory change có break moat không? (antitrust, GDPR-like, price control)

**⚠️ HONEST CORRECTION:**
> "Regulatory moat có durable không khi policy đổi?"
- Regulatory moat 2 chiều: bảo vệ incumbent NHƯNG cũng là risk nếu policy thay đổi (antitrust action, GDPR, drug price control, fintech charter reform)
- Flag: regulatory tailwind today có thể thành headwind tomorrow

**KPI watchlist:**
- License renewal status
- Regulatory inquiry/litigation pending
- Policy change trajectory (pro-incumbent or pro-disruption)
- Compliance cost as % revenue

---

### Frame 6 — Cyclicality / obsolescence analog ("đây là 1996 hay 1999?")

**Trigger condition**: Capex boom thesis, hype cycle (AI today, dot-com 1999, crypto 2017, EV 2021), tech-disruption story. User hoặc thesis claim "this time is different" hoặc "structural shift".

**Trigger phrasing:**
- "Đây là bong bóng không?"
- "Capex cycle có overshoot không?"
- "Đây là durable platform shift hay hype?"

**Template structure:**
1. **Capex/revenue gap** — Sequoia/Cahn-style analysis: tổng capex industry / actual revenue generated. Gap widen hay narrow?
2. **Demand durability** — multi-year structural (bull) vs cyclical (bear)? Evidence: scaling laws, adoption curve, Jevons paradox test
3. **Historical analog** — 4 analog:
   - AWS 2010-2020 (high-margin oligopol emerged) — bull
   - Telecom fiber 1998-2002 (WorldCom/Global Crossing overbuild bankrupt) — bear
   - Oil refining (cyclical commodity) — bear
   - Semiconductor foundry TSMC (extreme barrier monopoly) — opposite
4. **3-scenario verdict** — Bull (durable demand, capex earn return) / Base (partial overshoot) / Bear (oversupply, crash)

**⚠️ HONEST CORRECTION:**
> "Đây là durable platform shift hay泡沫?"
- Frame both honest: demand durable (bull wins on demand) COMPATIBLE WITH capex overshoot (bear wins on returns). Hai điều không loại nhau.
- Flag timing: scarcity persist đến khi nào? Supply catch up khi nào?

**KPI watchlist:**
- Industry capex trajectory
- Industry revenue (catching up to capex or widening gap?)
- Pricing trend ($/unit — rising = scarcity, falling = commodity)
- Scarcity end date (analyst consensus)

---

### Frame 7 — Capital allocation quality

**Trigger condition**: Công ty có phức tạp capital allocation — buyback lớn, M&A heavy, dividend, capex boom. Buffett-style "does management create value per dollar retained?"

**Trigger phrasing:**
- "Buyback có tạo value không?"
- "Capital allocation tốt không?"
- "M&A có destroy value không?"
- "ROIC vs WACC?"

**Template structure:**
1. **Capital allocation scorecard**:
   - ROIC vs WACC (return on invested capital > cost?)
   - Buyback timing (buying high or low? at what P/E?)
   - M&A track record (accretive or dilutive? goodwill impairment history?)
   - Dividend sustainability (payout ratio vs FCF)
   - Debt discipline (leverage trajectory)
   - Capex ROIC (capex generating revenue/lint?)
2. **Buffett test** — "ten-year retained earnings vs market cap gain" — $1 retained → >$1 market value created?
3. **Insider alignment** — management ownership, compensation structure, track record

**⚠️ HONEST CORRECTION:**
> "Capital allocation tạo value hay destroy value?"
- Buyback thường được sell-side cheerlead NHƯNG nếu buyback ở P/E cao + funded by debt → destroy value. Check buyback timing vs valuation.
- M&A goodwill impairment là sign honest của overpayment.

**KPI watchlist:**
- ROIC vs WACC trend
- Buyback $ vs P/E at time of buyback
- Goodwill impairment history
- Debt/EBITDA trajectory

---

### Frame 8 — Platform / ecosystem moat (network effect)

**Trigger condition**: Công ty có platform/network effect (Apple iOS, Microsoft Windows/Office, Visa/Mastercard network, Amazon marketplace, Google search-ads). User hoặc thesis claim "ecosystem"/"network effect"/"lock-in".

**Trigger phrasing:**
- "Network effect có durable không?"
- "Ecosystem có self-reinforcing không?"
- "Lock-in platform có mạnh không?"

**Template structure:**
1. **2-sided network analysis** — platform có 2+ sides (users + developers, buyers + sellers, cardholders + merchants)? Cả 2 sides growing?
2. **Switching cost breakdown** — data gravity, integration, learning curve, partner ecosystem, transaction cost to switch
3. **Developer/partner ecosystem** — size, growth, dependency (concentration risk nếu few big partners)
4. **Network effect type** — direct (more users = more value), indirect (complementors), data (more data = better product), platform (standards lock-in)

**⚠️ HONEST CORRECTION:**
> "Network effect có self-reinforcing không, hay fragility ẩn?"
- Network effects có thể reverse (network loss) — MySpace, BlackBerry, eBay collapsed khi tipping point cross
- Flag: switching cost có đang DECREASE không (open standards, regulation forcing interoperability)? Bundle lock-in vs standalone value?

**KPI watchlist:**
- Both sides engagement growth
- Switching cost trend (regulatory/tech decreasing?)
- Developer ecosystem health
- Network effect strength (data flywheel, complementor count)

---

### Frame 9 — Pricing power / brand premium (Consumer/Retail/Luxury)

**Trigger condition**: Công ty có pricing power rõ rệt (Coca-Cola, Apple, LVMH, Ferrari, Nike, Starbucks) — premium pricing trong commodity-ish market, hoặc brand moat. User hoặc thesis claim "pricing power" hoặc "brand moat".

**Trigger phrasing:**
- "Công ty có raise price mà không mất khách không?"
- "Brand có tạo premium không?"
- "Pricing power có durable không?"

**Template structure:**
1. **Price elasticity test** — historical: đã raise price X%, volume impact Y%. Elastic hay inelastic?
2. **Brand equity breakdown** — awareness, loyalty, perceived quality, associations. BrandZ/Interbrand ranking nếu có
3. **Premium vs substitute** — price per unit vs generic/competitor, premium %, trend (narrowing/widening?)
4. **Pricing power source** — brand? patent? switching cost? network effect? scarcity?

**⚠️ HONEST CORRECTION:**
> "Pricing power đến từ brand hay habit/inertia? Brand có transferable không?"
- Case distinction: brand premium (Apple, LVMH) vs inertia/availability (Coca-Cola in restaurants). Inertia fragile.
- Flag: private label gaining share? (Costco Kirkland, Amazon Basics, retailer brands)

**KPI watchlist:**
- Price/volume mix trend
- Gross margin trend
- Private label share in category
- Brand equity ranking trend

---

### Frame 10 — Secular tailwind / demographic shift

**Trigger condition**: Công ty hưởng lợi từ mega-trend dài hạn (aging population for healthcare, urbanization, decarbonization, digital transformation, emerging market middle class). User hoặc thesis claim "secular tailwind" hoặc "structural shift".

**Trigger phrasing:**
- "Công ty hưởng lợi từ [mega-trend] không?"
- "Trend này có durable không?"
- "Đây là secular hay cyclical?"

**Template structure:**
1. **Trend quantification** — CAGR của trend, timeline, data sources (census, IEA, WHO, McKinsey)
2. **Company exposure %** — bao nhiêu % revenue thực sự gắn với trend? Pure-play hay partial?
3. **Trend vs stock narrative gap** — trend có thể durable NHƯNG công ty có phải best way để play không?
4. **Trend risks** — policy reversal (climate), technology disruption (fossil fuel), demographic surprise

**⚠️ HONEST CORRECTION:**
> "Trend có durable NHƯNG công ty có phải best way để play trend không?"
- Case: solar/EV trend durable NHƯNG nhiều công ty bankrupt dọc đường (Solyndra, Nikola,QuantumScape)
- Flag: "trend đúng ≠ công ty này thắng" —区分 trend vs winner

**KPI watchlist:**
- Trend growth rate actual vs forecast
- Company market share in trend
- Trend policy/regulatory support
- Substitute/competing technologies

---

### Frame 11 — M&A / conglomerate discount (conglomerate, serial acquirer)

**Trigger condition**: Công ty phức tạp do nhiều M&A (BRK, CRM history, Verizon/Yahoo, InBev), hoặc trading at conglomerate discount. User hoặc thesis claim "sum of parts" hoặc "conglomerate discount".

**Trigger phrasing:**
- "Sum of parts worth hơn current market cap không?"
- "Conglomerate discount bao nhiêu?"
- "Spin-off có unlock value không?"

**Template structure:**
1. **Segment-by-segment valuation** — each business unit valued separately (P/E, EV/EBITDA peer-based). Sum vs market cap.
2. **Conglomerate discount %** — discount của current price so với sum-of-parts. Historical range.
3. **M&A track record** — accretive vs dilutive. Goodwill impairment history. Capital allocation score.
4. **Catalyst for value unlock** — spin-off, activist, simplification, divestiture

**⚠️ HONEST CORRECTION:**
> "Discount có thể justified — complexity, capital allocation, cross-subsidy risk"
- Conglomerate discount có thể be real opportunity (Buffett's BRK) HOẶC justified discipline (GE pre-breakup)
- Flag: who's the operator? Buffett-style vs conglomerate that destroys value (ViacomCBS, GE)

**KPI watchlist:**
- Sum-of-parts vs market cap gap
- M&A ROIC trend
- Goodwill as % of assets
- Activist involvement / spin-off rumors

---

### Frame 12 — Secular decline / disruption risk (bear-side)

**Trigger condition**: Công ty trong ngành bị disrupt (traditional retail vs Amazon, cable vs streaming, print media, fossil fuel, legacy software vs SaaS). User hoặc thesis concerned về "sunset" hoặc "decline".

**Trigger phrasing:**
- "Công ty có bị disrupt không?"
- "Ngành có đang suy giảm không?"
- "Legacy business có collapse không?"

**Template structure:**
1. **Disruptor mapping** — ai đang disrupt? Tốc độ? Technology, business model, regulatory.
2. **Company response analysis** — pivot (Netflix DVD→streaming), defend (Blockbuster), ignore (Sears). Execution?
3. **Cannibalization vs growth** — new business có bù đắp legacy decline không? Tốc độ?
4. **Time horizon** — decline rõ trong 3 năm, 5 năm, hay 10 năm?

**⚠️ HONEST CORRECTION:**
> "Disrupt có thể chậm hơn expectation — incumbent có thể sống lâu với FCF"
- Case: cable companies disrupted by streaming NHƯNG broadband business still strong; newspapers declining 20+ years but still profitable
- Flag: "disrupted eventually" ≠ "tomorrow" — value investors có thể profit từ "too cheap relative to FCF"

**KPI watchlist:**
- Legacy business decline rate
- New business growth
- Total revenue/FCF trajectory
- Management pivot execution

---

## C. Workflow dùng frames ở Phase 2

Với mỗi frame đã confirm ở Phase 0:

1. **Read** template section (A hoặc B ở trên)
2. **Fill** với data Phase 1 (research thật, citation footnote)
3. **Generate "honest correction"** — BẮT BUỘC. Tự hỏi: "Cách đọc nào ĐƠN GIẢN NHẤT mà bull case thường claim? Cách đọc đó có đúng không? Data có challenge nó không?"
4. **Verdict** + confidence (high/medium/low). Honest nếu uncertain.
5. **KPI watchlist** 3-5 điểm cụ thể để user theo dõi thesis đúng/sai trong 3-5 năm
6. **"Reframe cho nhà đầu tư X-K USD"** closer — gắn insight với quyết định vốn đầu tư

**Output mỗi frame = 1 section HTML** (id `sec-insight-N`), 6-8 sub-blocks, theo pattern `references/dashboard_design.md`.

## D. Anti-patterns (KHÔNG được làm)

- ❌ **Cheerlead** — insight chỉ bullish, không challenge. Fix: honest correction BẮT BUỘC.
- ❌ **Generic** — insight dùng cho mọi công ty, không đặc thù. Fix: data thật + company-specific examples.
- ❌ **Bịa data** — invent số liệu để fill template. Fix: NOT FOUND nếu không có, flag honest.
- ❌ **Copy Oracle** — clone ORCL insight verbatim. Fix: frames là skeleton, content fill per company.
- ❌ **Skip honest correction** — vì "thật ra bull case đúng mà". Fix: correction là differentiator, BẮT BUỘC dù correction reinforce bull.
- ❌ **Hardcode frames** — chạy fixed 3 frames cho mọi công ty. Fix: archetype router + user confirm.

## E. ✅ Quality checklist per insight section (BẮT BUỘC verify trước khi xong)

Trước khi hoàn thành mỗi insight section, verify checklist 8 điểm:

- [ ] **1. Trigger question rõ** — section-sub phrasing lại câu hỏi user/thesis (vd "X có phải trụ cột Y không?")
- [ ] **2. Data thật + citation** — mỗi số liệu quan trọng có footnote `<a class="ref">N</a>` ref tới numbered source
- [ ] **3. Frame structure follow** — 4-6 sub-block theo template (bảng + analysis + verdict)
- [ ] **4. Honest correction callout** — BẮT BUỘC có 1 callout `.callout.warn` hoặc `.callout.info` challenge bull reading đơn giản. Verbatim text: "Honest correction: ..."
- [ ] **5. Verdict + confidence** — rõ verdict (bull/bear/synth) + confidence level (high/medium/low). Honest nếu uncertain.
- [ ] **6. KPI watchlist 3-5 points** — cụ thể, measurable, theo dõi được quarterly
- [ ] **7. Reframe cho X-K USD** — closer gắn insight với vốn đầu tư tham chiếu
- [ ] **8. KHÔNG cheerlead** — nếu đọc xong chỉ thấy bull mà không challenge → fail checklist

## F. ⭐ Archetype Router expansion — Conglomerate + Emerging + Thesis-keyword fallback

### F.1 Conglomerate handler (BRK, GE-pre, JNJ-consumer spinoffs, 3M)

**KHÔNG auto-propose**. Skill **BẮT BUỘC hỏi user** ở Phase 0:

> "{TICKER} là conglomerate đa ngành. Skill cần focus sub-business nào để chọn insight frames phù hợp?"
>
> Options (multi-choice):
> 1. **Cash cow segment** (vd BRK insurance float, GE aviation) → frames 7 (capital alloc) + 5 (regulatory)
> 2. **Growth segment** (vd BRK BNSF railway, GE healthcare) → frames 1 (value-chain) + 8 (ecosystem)
> 3. **Equity portfolio** (vd BRK public stocks) → frames 7 (capital alloc) + 11 (sum-of-parts)
> 4. **Sum-of-parts / conglomerate discount** → frame 11
> 5. **All segments holistically** → frame 11 + 7

Skill dùng câu trả lời để route. KHÔNG đoán.

### F.2 Emerging sector / không có trong GICS router

**Sector examples**: drone (KVTO, ACHR), cannabis (TLRY, CGC), space (RKLB, SPCE), gene editing (CRSP, BEAM), quantum (IONQ, RGTI), plant-based meat (BYND)

**Handler**:
1. Skill **flag**: *"Sector {X} không có trong GICS default router. Để đề xuất frames, skill cần biết:"*
2. Hỏi 1 câu:
   - "Công ty có platform/network effect không?" → frame 8
   - "Công ty có regulatory moat không?" → frame 5
   - "Sector đang trong hype cycle không?" → frame 6 (cyclicality)
3. **Default fallback nếu user không rõ**: frame 7 (capital allocation) + frame 2 (margin defensibility) — 2 frame tổng quát nhất apply mọi ngành.

### F.3 Thesis-keyword fallback (cho công ty chuyển mình)

**Examples**: TSLA (auto → AI/robotics), AMZN (retail → cloud), AAPL (hardware → services), DIS (media → streaming)

**Handler**:
- Nếu user's Phase 0 question hoặc thesis keyword gợi ý transformation:
  - "AI/automation" → frame 1 (value-chain) + frame 8 (ecosystem)
  - "Cloud/SaaS" → frame 2 (margin) + frame 3 (contract/backlog)
  - "Platform/ecosystem" → frame 8
  - "Energy transition" → frame 6 (cyclicality) + frame 10 (secular)
  - "Recovery/turnaround" → frame 7 (capital alloc) + frame 12 (secular decline)
- Skill **đề xuất dựa keyword** + user confirm

### F.4 Bull market vs bear market skill mode

Skill cũng detect market regime (S&P 500 vs 200-day MA, VIX) để tune tone:
- **Bull market**: bias nhẹ về frame 6 (cyclicality — tránh FOMO) + frame 12 (disruption risk)
- **Bear market**: bias nhẹ về frame 7 (capital allocation —谁 survives) + frame 8 (ecosystem — incumbent优势)
- Không phải hard rule, chỉ là nudge.

## G. 12-frame quick reference (tóm tắt)

| # | Frame name | 1-line trigger | Key question |
|---|---|---|---|
| 1 | Value-chain positioning | Part of hot value chain (AI/EV/semis) | Có phải "trụ cột" không? |
| 2 | Margin defensibility / barriers | Biên thấp hoặc capex-heavy | Ai vào thay được không? |
| 3 | Contract / backlog moat | RPO/backlog là KPI headline | Tạo fleet fungible hay pass-through? |
| 4 | Counterparty / concentration risk | 1 khách lớn drive thesis | Khách có trả được nợ không? |
| 5 | Regulatory / compliance moat | Regulated industry | Moat durable khi policy đổi? |
| 6 | Cyclicality / obsolescence analog | Capex boom, hype cycle | 1996 hay 1999? |
| 7 | Capital allocation quality | Phức tạp buyback/M&A/dividend | Tạo hay destroy value? |
| 8 | Platform / ecosystem moat | Network effect | Self-reinforcing hay fragile? |
| 9 | Pricing power / brand premium | Premium brand, raise price được | Brand hay inertia? Private label threat? |
| 10 | Secular tailwind / demographic | Mega-trend (aging, decarbon) | Best way to play trend? |
| 11 | M&A / conglomerate discount | Multi-segment, sum-of-parts | Discount justified hay opportunity? |
| 12 | Secular decline / disruption | Legacy industry disrupted | Khi nào collapse? FCF still value? |

---

## H. Commodity-specific metrics extensions (mới sau NEM test 7/2026)

> ⭐ **Học từ NEM**: Archetype router hiện tại không có sector match cho gold mining (Basic Materials).
> Skill dùng Edge Case Handler + thesis keyword để chọn frames — OK NHƯNG frames template chung chung,
> không có指引 cho **metrics đặc thù commodity**. Section này bổ sung.

### H.1 Gold / metals mining (NEM, AEM, B, KGC, AU, FCX)

**Metrics cần bổ sung vào insight + valuation sections:**

| Metric | Vì sao quan trọng | NEM benchmark |
|---|---|---|
| **AISC ($/oz)** | All-In Sustaining Cost = chi phí thật 1 oz. Quan trọng nhất cho margin analysis | $1,358 (2025), guide $1,680 (2026) |
| **By-product vs co-product AISC** | By-product trừ doanh thu phụ (đồng/bạc) khỏi cost → thấp hơn. Cùng baseline khi so peer | Gap $251/oz cho NEM |
| **Reserves (Proven & Probable, Moz)** | Trữ lượng xác định. Tương đương RPO của SaaS nhưng hữu hạn | 118.2Moz (~20 năm life) |
| **Reserve life (năm)** | Reserves / annual production. >10 năm = an toàn | ~20 năm (NEM) |
| **Grade (g/t)** | Hàm lượng vàng trong quặng. Decline −7-13%/decade ngành | — |
| **Production attributable (Moz)** | Sản lượng attributable (sau JV%) | 5.9Moz (NEM 2025) |
| **P/NAV (Price/Net Asset Value)** | NPV trữ lượng tại giá vàng thận trọng. **Chuẩn nhất cho miner**, P/E bị chu kỳ méo | ~25% discount (NEM) |
| **P/FCF** | Price / Free Cash Flow. FCF > Net income cho miner (D&A lớn) | FCF yield ~7% (NEM) |

**Frames ưu tiên cho gold mining** (Priority khi Phase 0 archetype routing):
1. **Frame 6 (Cyclicality)** — gold price cycle, "1996 hay 1999?" analogy
2. **Frame 2 (Margin defensibility)** — AISC quartile, by-product structure
3. **Frame 11 (M&A/sum-of-parts)** — reserves acquisition, portfolio optimization

**⚠️ Đặc biệt chú ý:**
- **P/E = CYCLICAL VALUE TRAP**: P/E thấp ở đỉnh giá vàng (EPS cao), N/A ở đáy (EPS âm). Dùng P/NAV + EV/EBITDA + FCF yield thay P/E.
- **AISC scale với giá vàng**: royalty % structure → AISC tự tăng khi giá tăng, ăn mòn đòn bẩy
- **By-product credit risk**: nếu giá đồng/bạc giảm, AISC by-product tăng
- **Reserve depletion**: mỗi năm khai thác → phải explore/acquire bổ sung. Grade decline structural.
- **Streaming/royalty (WPM, FNV) là model khác hoàn toàn**: AISC ~$0, margin >75%, P/E 30× — không compare trực tiếp với miners.

### H.2 Oil & gas (XOM, CVX, COP, OXY, EOG, PXD)

**Metrics cần bổ sung:**

| Metric | Vì sao quan trọng |
|---|---|
| **WTI / Brent price** | Spot price driver chính |
| **Production (boe/day)** | Barrel of oil equivalent |
| **Reserves (Bboe)** | Proved reserves |
| **Reserve replacement ratio** | % production replaced by new reserves/năm. >100% = healthy |
| **Lifting cost ($/boe)** | Cost khai thác 1 barrel |
| **Finding & Development cost ($/boe)** | Cost phát hiện + phát triển mỏ mới |
| **Cash flow from operations / barrel** | Margin thật |
| **EV/EBITDA, P/CF** | Chuẩn hơn P/E (D&A lớn) |
| **Refining crack spread** (integrated) | Margin lọc dầu |

**Frames ưu tiên**: 6 (cyclicality — oil price), 2 (margin — lifting cost quartile), 11 (M&A).

### H.3 Agriculture / soft commodities (ADM, BG, INGR)

Ít phổ biến cho retail investor. Bỏ qua trong scope này.

### H.4 Khi gặp sector commodity mới không có ở đây

**Handler Phase 0**: nếu archetype routing không match:
1. Flag "commodity sector, không có metric guide cụ thể"
2. Hỏi user: "Công ty có metric đặc thù nào (AISC, lifting cost, fleet utilization...) cần track?"
3. Default: dùng P/CF + EV/EBITDA + Frame 6 (cyclicality) + Frame 2 (margin)
4. Luôn flag: **"P/E cho commodity producer có thể là bẫy chu kỳ — verify EPS ở đâu trong cycle"**
