# Language Layers — 3-layer cho readable retail

> Pattern làm báo cáo accessible cho nhà đầu tư cá nhân. Đọc ở Phase 4.

## 3 layers (chạy song song)

### Layer 1: Glossary (Section 21)

**Structure**: 2 cards — "Thuật ngữ tài chính" (12 term cố định) + "Thuật ngữ [DOMAIN]" (12 term động per company).

#### Card 1: Financial terms (CỐ ĐỊNH — copy/paste)
```
EPS, P/E, P/B, FCF, GAAP vs non-GAAP, Capex, RPO/Backlog, OCF, Buyback, Dilution, Drawdown, DCA
```
Mỗi term: định nghĩa ngắn + ví dụ với **số liệu thực của công ty đang phân tích** (KHÔNG dùng số Oracle hardcoded — điền `[EPS hiện tại của TICKER] × [số cổ phiếu] = [số tiền]/năm thuộc về bạn`).

#### Card 2: Domain terms (ĐỘNG per company)
12 term đặc thù doanh nghiệp/ngành. Examples:
- **Tech/Semis**: GPU, TSMC, CoWoS, HBM, ASIC, FPGA, design win, node, foundry, EUV, tape-out, yield
- **Software/Cloud**: ARR, NRR, SBC, take rate, consumption-based, SaaS, IaaS, PaaS, multicloud, hybrid, churn, land-and-expand
- **Banks**: NIM, ROE, ROA, Tier-1 capital, NPL, efficiency ratio, deposit beta, loan loss provision, CET1, NCO rate, loan-to-deposit, loan yield
- **Healthcare**: Pipeline, Phase 1/2/3, PDUFA, FDA, EMA, patent cliff, R&D pipeline, biologic, generic, OTC
- **REITs**: FFO, AFFO, NAV, cap rate, WALE, occupancy, NOI, same-property cash flow
- **Energy**: Reserve, EV/EBITDA, P/CF, crack spread, WTI/Brent, refining margin, production volume
- **Gold/Metals mining** (NEM, AEM, B, KGC, AU): AISC, by-product vs co-product, reserves (P&P), reserve life, grade (g/t), P/NAV, streaming/royalty, Tier-1 asset

### Layer 2: 💡 "Nói cách khác" callouts

**Placement** (BẮT BUỘC ở 4-6 chỗ):
1. **Executive Summary (Section 2)** — "Nói cách khác — bản dịch cho người mới": tóm thesis bằng tiếng Việt đơn giản
2. **Valuation verdict (Section 8)** — "Nói cách khác": giải thích verdict 3-zone không dùng jargon
3. **Mỗi Insight conclusion** — 1 callout cuối mỗi Special Insight
4. **Moat conclusion (nếu có Frame 2)** — "Nói cách khác": rào cản thực tế translate
5. **33K Lens conclusion** — "Nói cách khác": framework DCA đơn giản
6. **Top "3 ý quan trọng nhất" ở đầu Glossary** — onboarding cho người mới

**CSS class**: `.callout.plain` (amber border-left, slightly tinted background). Title pattern: `💡 Nói cách khác — bản dịch cho người mới` hoặc `💡 Nói cách khác:` inline.

**Tone**:
- Dùng đời thường analog ("Oracle giống chủ nhà", "như cổ phiếu thay vì trả lãi")
- Tránh thuật ngữ khi có thể (EPS → "lợi nhuận trên mỗi cổ phiếu")
- Sentence ngắn, dễ hiểu cho người mới

**Anti-pattern**:
- ❌ Dịch từng từ (CPU → "đơn vị xử lý trung tâm" — giữ CPU)
- ❌ Hạ thấp người đọc chuyên sâu (callout phụ, không thay thế content chính)
- ❌ Quá nhiều callout (chỉ ở conclusion đặc, không mỗi paragraph)

### Layer 3: Jargon kept (correct usage)

**Giữ nguyên** tên riêng/chữ viết tắt chuẩn — không dịch:
- Tên công ty (Oracle, NVIDIA, Microsoft)
- Tên sản phẩm (Oracle Database, OCI, AWS, Azure)
- Chữ viết tắt chuẩn (EPS, P/E, P/B, GPU, CPU, AI, FY, YoY, QoQ, MA, RSI, MACD)
- Thuật ngữ kỹ thuật chuẩn (volatility, drawdown, beta, correlation)

**Footnote khi first use** hoặc giải thích ở glossary. Không giải thích lại mỗi lần xuất hiện.

## Pattern thực thi

1. **Viết content chính** với jargon chuẩn (cho người chuyên sâu)
2. **Thêm glossary section** với 12+12 term
3. **Thêm 💡 callout** ở 4-6 conclusion point — "bản dịch" cho người mới
4. **Verify**: người mới đọc section 2 (TL;DR) + glossary + 💡 callouts → hiểu được thesis; người chuyên sâu đọc full → thấy đủ depth

## Anti-pattern tổng

- ❌ Dịch "EPS" thành "lợi nhuận trên mỗi cổ phiếu" trong content chính (chỉ ở glossary)
- ❌ Quá nhiều 💡 callout (mất tính professional)
- ❌ Quá ít 💡 callout (không accessible)
- ❌ Glossary cố định 12 term domain giống mọi công ty (phải per-company)
