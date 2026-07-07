# Dashboard Design — Section map + CSS + Chart.js wiring

> Đọc ở Phase 5 (render). Template tokenized tại `assets/dashboard_template.html`.

## A. 22-section map (canonical order)

| # | id | Title | Generic/Dynamic |
|---|---|---|---|
| 1 | `sec-hero` | Hero + KPI strip (6 KPIs) | Generic |
| 2 | `sec-exec` | Executive Summary (4 callouts + 💡) | Generic |
| 3 | `sec-biz` | Business 101 — how makes money | Generic |
| 4 | `sec-industry` | Industry Position (3 layers) | Generic |
| 5 | `sec-history` | Financial History 10 năm | Generic |
| 6 | `sec-segment` | Segment Analysis | Generic |
| 7 | `sec-thesis` | Investment Thesis 3-5y + conditions + KPI | Generic |
| 8 | `sec-valuation` | Valuation — P/E P/B vs 5Y/10Y | Generic |
| 9 | `sec-peer` | Peer Comparison (scatter) | Generic |
| 10 | `sec-bs` | Balance Sheet, Capex & FCF | Generic |
| 11 | `sec-risk` | Risk Matrix (14 risks) | Generic |
| 12 | `sec-33k` | X-K USD lens (lump vs DCA, drawdown, checklist) | Generic |
| 13 | `sec-scenario` | Scenario Analysis (Bull/Base/Bear) | Generic |
| 14 | `sec-checklist` | Final Investment Checklist | Generic |
| 15-17 | `sec-insight-{N}` | **[DYNAMIC — from Phase 2]** 1-4 Special Insight | **Dynamic** |
| 18 | `sec-tech` | Technical — Mode ACTIVE | Generic |
| 19 | `sec-tech-profile` | Technical — Mode PROFILE (NON-ADVICE) | Generic |
| 20 | `sec-analyst` | Analyst Synthesis | Generic |
| 21 | `sec-glossary` | Glossary | Generic |
| 22 | `sec-source` | Source Appendix + Data Quality | Generic |

**Plus**: TOC section right after hero (`sec-toc`), no number.

## B. CSS — hybrid dark theme (Bloomberg-ish)

```css
:root{
  --bg-0:#0f1419; --bg-1:#13181f; --bg-2:#1a2029;
  --card:#161b22; --card-2:#1c232d;
  --border:rgba(255,255,255,0.08); --border-hot:rgba(245,166,35,0.45);
  --text:#e6edf3; --text-dim:#8b949e; --text-faint:#565f6b;
  --amber:#f5a623; --amber-soft:rgba(245,166,35,0.14);
  --blue:#4a9eff; --blue-soft:rgba(74,158,255,0.14);
  --green:#3fb950; --green-soft:rgba(63,185,80,0.14);
  --red:#f85149; --red-soft:rgba(248,81,73,0.14);
  --purple:#a78bfa; --purple-soft:rgba(167,139,250,0.14);
  --grad-amber:linear-gradient(135deg,#f5a623 0%,#d48806 100%);
  --grad-blue:linear-gradient(135deg,#4a9eff 0%,#2670c8 100%);
  --font-sans:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
  --font-mono:'JetBrains Mono',ui-monospace,'SF Mono',Menlo,monospace;
  --radius:12px; --radius-sm:8px;
}
```

**Theme**: hybrid dark sạch — accent amber + xanh dương, viền mảnh, ít glow. Theo user chọn ORCL.

**Class names chuẩn** (xem `assets/dashboard_template.html` cho full CSS):
- Layout: `.container`, `.grid-2`, `.grid-3`, `.grid-4`, `.grid-2-1`, `.grid-1-2`
- Section: `.section`, `.section-title`, `.num`, `.tag.amber/.blue/.green/.red/.purple`, `.divider`, `.section-sub`
- Hero: `.hero`, `.ticker-badge`, `.company-name`, `.kpi-strip`, `.kpi`, `.kpi-label/.kpi-value/.kpi-delta`
- Card: `.card`, `.card-head`, `.card-title`, `.card-sub`, `.chart-wrap` (+ `.sm/.lg/.xs`)
- Table: `.fin-table`, `.col-latest`, `.row-strong`, `.table-wrap`
- Callout: `.callout` (+ `.warn/.good/.info/.neu/.plain`)
- Glossary: `.glossary-grid`, `.gloss-item`, `.gloss-term`, `.gloss-def`
- TOC: `.toc-panel`, `.toc-grid`, `.toc-item`, `.toc-num`, `.toc-text`, `.toc-label`, `.toc-desc`
- xref: `a.xref`
- Tech: `.tech-score-card`, `.tech-score-num`, `.tech-verdict-pill`, `.signal-grid`, `.signal-cell`
- Profile: `.non-advice-panel`
- Risk: `.risk-table`, `.pill.pill-l/.pill-m/.pill-h`
- Scenario: `.scenario-grid`, `.scenario-card.bull/.base/.bear`
- Ref: `.refs`, `.ref`, `.src-meta`
- Check: `.check-list`, `.check-box.on/.off`
- Quality: `.qbadge.qbadge-HIGHQ/.qbadge-MEDQ/.qbadge-LOWQ`

## C. Chart.js wiring pattern

**Library**: Chart.js 4.4.1 + chartjs-plugin-annotation 3.0.1 (CDN).
**Fonts**: Inter + JetBrains Mono (Google Fonts).

**Wiring helper**:
```js
Chart.defaults.color = '#8b949e';
Chart.defaults.font.family = "'Inter', sans-serif";
Chart.defaults.borderColor = 'rgba(255,255,255,0.05)';

const AMBER='#f5a623', BLUE='#4a9eff', GREEN='#3fb950', RED='#f85149', PURPLE='#a78bfa';
const baseScales = { x:{grid:{display:false}}, y:{grid:{color:'rgba(255,255,255,0.05)'}} };
function grad(ctx, c1, c2){ /* linear gradient fill */ }
const baseOpts = (extra) => ({ responsive:true, maintainAspectRatio:false, plugins:{...}, ...extra });

new Chart(canvas, { type, data, options: baseOpts({...}) });
```

**Standard charts** (~13 total):
1. Revenue + Net Income (bar + line, dual axis)
2. Capex vs FCF (bar + line)
3. Segment mix (doughnut)
4. RPO growth (bar)
5. Capex trajectory forward (bar)
6. P/E history with avg bands (line + annotation)
7. Debt vs Cash (bar + line)
8. Dividend + Buyback (stacked bar)
9. Peer scatter P/E vs growth (bubble)
10. Technical Price + MA (line)
11. Technical RSI (line + overbought/oversold bands)
12. Profile Drawdown (line)
13. Profile Distribution histogram (bar)

## D. TOC + xref auto-generation (Python helper)

**Pattern đã chứng minh với ORCL** — áp dụng cho mọi ticker.

### Build TOC
1. Scan `<section id="sec-...">` → list of (id, label, desc)
2. Map section number → id
3. Generate `<a class="toc-item" href="#{id}"><span class="toc-num">{N}</span><span class="toc-text"><span class="toc-label">{label}</span><span class="toc-desc">{desc}</span></span></a>`
4. Wrap in `<section id="sec-toc"><div class="toc-panel">...<div class="toc-grid">{items}</div></div></section>`
5. Insert after hero section close

### Convert "Section N" refs → clickable
1. Map number → section id (semantic — "Section N" trong text mean thứ N theo canonical order)
2. Tokenize HTML: split tag vs text chunks
3. In TEXT chunks only: regex `Section\s+(\d{1,2})(\.\d+)?(?!\s*[-–—]\d)` → `<a href="#{id}" class="xref">{full}</a>`
4. Skip ranges (Section 5-10) — leave as text

**Caveat**: NUMBER mapping phải khớp canonical order. Nếu render skip section (`--no-technical`), số shift → cần re-map. Safest: dùng **id** thay vì number khi refer.

## E. Token replace (str.replace, KHÔNG f-string)

```python
TOKEN_MAP = {
    '{{TICKER}}': ticker,
    '{{COMPANY_NAME}}': company_name,
    '{{COMPANY_SUB}}': f"{exchange} · {sector}",
    '{{PRICE}}': price,
    '{{PRICE_DATE}}': price_date,
    '{{MARKET_CAP}}': market_cap,
    '{{KPI_STRIP}}': kpi_strip_html,
    '{{HISTORY_DATA}}': json.dumps(history_data),
    '{{PEER_DATA}}': json.dumps(peer_data),
    '{{INSIGHT_SECTIONS}}': insight_sections_html,
    '{{GLOSSARY_DOMAIN}}': glossary_domain_html,
    '{{REFS_LIST}}': refs_list_html,
    '{{DATA_QUALITY_MATRIX}}': dq_matrix_html,
    '{{CAPITAL_AMOUNT}}': str(capital),
    '{{FY_LABEL}}': fy_label,
    '{{ANALYST_TABLE}}': analyst_table_html,
    # ... etc
}
for token, value in TOKEN_MAP.items():
    html = html.replace(token, str(value))
```

**Verify**: `grep -oE "\{\{[A-Z_0-9]+\}\}"` rỗng sau fill.

## F. Quality gates checklist (Phase 6)

- [ ] 22 sections (hoặc 17-19 nếu `--no-technical`/`--no-analyst`/`--fundamental-only`)
- [ ] TOC panel đầy đủ, click hoạt động
- [ ] xref links auto-generated, no plain "Section N" standalone (chỉ ranges OK)
- [ ] `node --check` inline JS OK
- [ ] `grep "\{\{[A-Z_]+\}\}"` rỗng (no unreplaced tokens)
- [ ] `grep non-advice` trong section PROFILE (19) rỗng: `grep -iE "bullish|bearish|khuyến nghị mua|khuyến nghị bán|strong buy|strong sell|tín hiệu vào|tín hiệu ra"` → empty
- [ ] Mỗi số liệu lớn có footnote `<a class="ref">`
- [ ] Insight sections có "honest correction" callout
- [ ] GAAP vs non-GAAP specified khi dùng P/E
- [ ] Fiscal year flag rõ (FY/CY)
- [ ] NOT FOUND / NOT VERIFIED marked honest
- [ ] KHÔNG có "khuyến nghị mua/bán" tuyệt đối
- [ ] Mobile responsive (grid collapses)
- [ ] Browser smoke test (optional)

## G. Deploy Vercel

```bash
mkdir -p ~/ZCodeProject/{ticker-lowercase}-deploy
# write index.html
/Users/bobo/.local/bin/vercel deploy ~/ZCodeProject/{ticker-lowercase}-deploy --prod -y
# timeout 600000ms
```

CLI đã auth `thanhtran-165` (team `team_dRh23vUGV5tRJlNjlDQelq2E`). Auto-link project, generate `.vercel/project.json`.

Return URL: `https://{project-name}.vercel.app`.

## Xref cross-reference links (BẮT BUỘC — v2.2.6)

Mỗi "Section N" trong text PHẢI là `<a href="#sec-..." class="xref">Section N</a>`. ORCL benchmark có 31 xref. Verify: `grep -c 'class="xref"'` ≥ 10 trước deploy.

Section map: 1=sec-hero, 2=sec-exec, 3=sec-biz, 4=sec-industry, 5=sec-history, 6=sec-segment, 7=sec-thesis, 8=sec-valuation, 9=sec-peer, 10=sec-bs, 11=sec-risk, 12=sec-33k, 13=sec-scenario, 14=sec-checklist, 15-17=sec-insight/moat/supply, 18=sec-tech, 19=sec-tech-profile, 20=sec-analyst, 21=sec-glossary, 22=sec-source.
