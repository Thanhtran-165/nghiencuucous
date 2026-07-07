# Dashboard Assets

## Files

| File | Purpose |
|---|---|
| `dashboard_skeleton.html` | **⭐ WORKING TEMPLATE (primary)** — skeleton sạch (~58KB, 105 tokens), chỉ CSS + JS + section structure + disclaimer + sidebar layout. LLM fill `{{TOKEN}}` per ticker. **DÙNG FILE NÀY LÀM TEMPLATE.** |
| `_REFERENCE_ORCL_DONT_USE_AS_TEMPLATE.html` | **⚠️ REFERENCE ONLY — KHÔNG DÙNG LÀM TEMPLATE** — báo cáo ORCL hoàn chỉnh (248KB, 22 sections). Chỉ để xem depth/quality benchmark + pattern cụ thể. Tên file có `_DONT_USE_AS_TEMPLATE` để LLM không nhầm. |

## Đã xóa (legacy)

- ~~`dashboard_template.html`~~ — đã xóa 7/2026. File này là ORCL report với title tokenized, chứa 222 Oracle content → nếu dùng làm template sẽ inherit Oracle content (silent failure). Skeleton thay thế hoàn toàn.

## Cách dùng (Phase 5 render)

### Bước 1: Copy SKELETON (KHÔNG copy example)

```python
import shutil
shutil.copy(
    "~/.zcode/skills/us-equity-research/assets/dashboard_skeleton.html",  # ⭐ SKELETON
    f"~/ZCodeProject/{ticker_lower}-deploy/index.html"
)
# ❌ KHÔNG copy _REFERENCE_ORCL_DONT_USE_AS_TEMPLATE.html
# ❌ KHÔNG copy orcl-deploy/index.html (nếu đã deploy Oracle trước đó)
```

**Tại sao không copy orcl-deploy**: orcl-deploy là báo cáo Oracle hoàn chỉnh, chứa 200+ Oracle-specific content. Nếu copy → phải thay từng đoạn → dễ sót. Skeleton sạch 100%, chỉ có CSS + JS + structure.

### Bước 2: Fill tokens via str.replace (KHÔNG f-string)

```python
TOKEN_MAP = {
    "{{TICKER}}": ticker,
    "{{COMPANY_NAME}}": company_name,
    "{{COMPANY_SUB}}": f"{exchange} · {sector} · FY ends {fy_end} · HQ {hq}",
    "{{HERO_INTRO}}": f"Investment evidence pack... vốn tham khảo ${capital:,}...",
    "{{PRICE}}": price,
    "{{PRICE_DATE}}": price_date,
    "{{PRICE_CCY}}": "$",
    "{{PRICE_DELTA}}": f"{delta_pct}%",
    "{{PRICE_DELTA_CLASS}}": "pos" if delta > 0 else "neg",
    # ... etc (105 tokens total)
}
for token, value in TOKEN_MAP.items():
    html = html.replace(token, str(value))
```

### Bước 3: Viết content per section

`_REFERENCE_ORCL_DONT_USE_AS_TEMPLATE.html` là **reference** cho depth + structure. Mỗi section trong reference có content đặc thù Oracle — **đọc pattern structure, KHÔNG copy content**. Viết fresh content per ticker dựa trên:
- Data đã research (Phase 1)
- Insight frames đã chạy (Phase 2)
- Sector-specific (GICS router + commodity extensions Section H)

### Bước 4: Generate TOC sidebar + xref

Skeleton đã có sẵn sidebar layout (CSS `.toc-sidebar`, `.layout-main`, `.layout-content`).
- **Sidebar TOC**: skeleton có placeholder `<aside class="toc-sidebar">` — fill list items với section ids
- **xref inline**: dùng `scripts/generate_toc_xref.py` (nếu có) HOẶC viết tay `<a href="#sec-..." class="xref">Section N</a>` trong text

### Bước 5: Quality gates

- `node --check` inline JS
- `grep -oE "\{\{[A-Z_0-9]+\}\}"` empty (no unreplaced tokens)
- `grep non-advice` empty trong section PROFILE (19)
- `grep -c "Oracle\|ORCL"` = 0 (no inherited Oracle content)
- 22 sections đầy đủ
- Citation footnotes cho số liệu quan trọng
- Disclaimer block có (CSS `.disclaimer`)
- Sidebar TOC có (CSS `.toc-sidebar`)

### Bước 6: Deploy

```bash
vercel deploy ~/ZCodeProject/{ticker-lowercase}-deploy --prod -y
```

## Structure preserved from ORCL example (trong skeleton)

- **CSS**: full hybrid dark theme (~320 lines) — Bloomberg-ish, accent amber + blue
- **CSS**: disclaimer block + sidebar layout (backport từ orcl-deploy 7/2026)
- **JS**: full Chart.js 4.4.1 + annotation plugin wiring, 13 chart patterns, nav/scroll-spy/progress
- **Section structure**: 22 sections with consistent id pattern (`sec-hero`, `sec-exec`, ...)
- **Component classes**: card, callout, fin-table, kpi, scenario-card, risk-table, disclaimer, toc-sidebar, ...

## What changes per ticker

- Hero KPI strip (6 cards từ data)
- All section content (text, tables, charts data)
- Special Insight sections (1-4 dynamic, from Phase 2 frames)
- Glossary "Domain" card (12 term per company)
- Analyst table + targets
- Refs list + Data Quality matrix

## Tokens to fill (priority)

| Token | Where | Type |
|---|---|---|
| `{{TICKER}}` | title, brand, throughout | string |
| `{{COMPANY_NAME}}` | title, hero, throughout | string |
| `{{COMPANY_SUB}}` | hero sub-line | string |
| `{{HERO_INTRO}}` | hero dim intro | string |
| `{{PRICE}}`, `{{PRICE_DATE}}`, `{{PRICE_CCY}}`, `{{PRICE_DELTA}}`, `{{PRICE_DELTA_CLASS}}` | hero price block | strings |
| `{{PRICE_META}}`, `{{PRICE_META_2}}` | hero market cap + dividend lines | strings |
| `{{KPI_STRIP}}` | 6 KPI cards | HTML block |
| `{{HISTORY_DATA}}`, `{{PEER_DATA}}`, etc. | JS data objects | JSON |
| `{{INSIGHT_SECTIONS}}` | 1-4 dynamic Special Insights | HTML block |
| `{{GLOSSARY_DOMAIN}}` | 12 domain terms | HTML block |
| `{{REFS_LIST}}` | numbered references | HTML block |
| `{{DATA_QUALITY_MATRIX}}` | HIGHQ/MEDQ/LOWQ table | HTML block |
| `{{CAPITAL_AMOUNT}}` | X-K lens capital | string |
| `{{ANALYST_TABLE}}`, `{{CONSENSUS_CARD}}` | analyst section | HTML block |

**Lưu ý**: không phải mọi chuỗi Oracle đều được đánh dấu token (sẽ quá nhiều). LLM đọc `_REFERENCE_ORCL` để biết pattern structure → viết lại content fresh per ticker. Token chỉ ở những chỗ phổ quát (title, brand, hero cơ bản).
