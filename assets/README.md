# Dashboard Assets

## Files

| File | Purpose |
|---|---|
| `dashboard_skeleton.html` | **⭐ WORKING TEMPLATE (primary)** — skeleton sạch (54KB, 105 tokens), chỉ CSS + JS + section structure. KHÔNG có Oracle content. LLM fill `{{TOKEN}}` per ticker. |
| `dashboard_example_orcl.html` | **Reference example** — báo cáo ORCL hoàn chỉnh (253KB, 22 sections, real data, real insight engine output). Dùng làm depth/quality benchmark + xem pattern cụ thể cho từng section. |
| `dashboard_template.html` | (legacy) ORCL report với title tokenized. Có thể xóa — skeleton thay thế. |

## Cách dùng (Phase 5 render)

### Bước 1: Copy template
```python
import shutil
shutil.copy(
    "~/.zcode/skills/us-equity-research/assets/dashboard_template.html",
    f"~/ZCodeProject/{ticker_lower}-deploy/index.html"
)
```

### Bước 2: Fill tokens via str.replace (KHÔNG f-string)
```python
TOKEN_MAP = {
    "{{TICKER}}": ticker,                       # e.g. NVDA
    "{{COMPANY_NAME}}": company_name,           # e.g. NVIDIA Corporation
    "{{COMPANY_SUB}}": f"{exchange} · {sector} · FY ends {fy_end} · HQ {hq}",
    "{{HERO_INTRO}}: f"Investment evidence pack... vốn tham khảo ${capital:,}...",
    "{{PRICE}}": price,
    "{{PRICE_DATE}}": price_date,
    "{{PRICE_CCY}}": "$",
    "{{PRICE_DELTA}}": f"{delta_pct}%",
    "{{PRICE_DELTA_CLASS}}": "pos" if delta > 0 else "neg",
    # ... etc
}
for token, value in TOKEN_MAP.items():
    html = html.replace(token, str(value))
```

### Bước 3: Viết content per section
ORCL example là **reference** cho depth + structure. Mỗi section trong example có content đặc thù Oracle — **đọc pattern structure, KHÔNG copy content**. Viết fresh content per ticker dựa trên:
- Data đã research (Phase 1)
- Insight frames đã chạy (Phase 2)
- Sector-specific (GICS router)

### Bước 4: Generate TOC + xref
```python
# Scan section ids → build TOC grid
# Convert "Section N" text → <a class="xref"> trong text chunks
# (xem references/dashboard_design.md section D)
```

### Bước 5: Quality gates
- `node --check` inline JS
- `grep -oE "\{\{[A-Z_0-9]+\}\}"` empty (no unreplaced tokens)
- `grep non-advice` empty trong section PROFILE
- 22 sections đầy đủ
- Citation footnotes cho số liệu quan trọng

### Bước 6: Deploy
```bash
vercel deploy ~/ZCodeProject/{ticker-lower}-deploy --prod -y
```

## Structure preserved from ORCL example

- **CSS**: full hybrid dark theme (~270 lines) — Bloomberg-ish, accent amber + blue
- **JS**: full Chart.js 4.4.1 + annotation plugin wiring, 13 chart patterns, nav/scroll-spy/progress
- **Section structure**: 22 sections with consistent id pattern (`sec-hero`, `sec-exec`, ...)
- **Component classes**: card, callout, fin-table, kpi, scenario-card, risk-table, etc.

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

**Lưu ý**: không phải mọi chuỗi Oracle đều được đánh dấu token (sẽ quá nhiều). LLM đọc ORCL example để biết pattern structure → viết lại content fresh per ticker. Token chỉ ở những chỗ phổ quát (title, brand, hero cơ bản).
