# us-equity-research — ZCode Skill nghiên cứu cổ phiếu Mỹ

ZCode skill nghiên cứu cổ phiếu Mỹ (NYSE/NASDAQ) đầy đủ — pipeline 7 phase: data → fundamental → valuation → **dynamic insight engine** → technical → analyst → dashboard HTML deploy Vercel.

## ⭐ Đặc trưng cốt lõi: Insight Engine động

Khác với báo cáo cố định, skill này **KHÔNG có "special insight" hardcoded**. Mỗi doanh nghiệp có câu chuyện chiến lược riêng → skill **tự đề xuất insight frames** dựa:

1. **Archetype router** (GICS sector → default frames)
2. **Tương tác user** (confirm / add / remove / tự đặt câu hỏi)
3. **12 insight frames** tổng quát (value-chain, margin defensibility, OpenAI risk, ecosystem moat, capital allocation, regulatory, v.v.)
4. **Honest correction BẮT BUỘC** mỗi frame — không cheerlead

## Cách dùng

```
/us-equity-research NVDA              # Phân tích đầy đủ NVIDIA
/us-equity-research AAPL              # Phân tích đầy đủ Apple
/us-equity-research MSFT --fundamental-only   # Bỏ technical + analyst + deploy
/us-equity-research TSLA --insights 2         # Override số insight frames
/us-equity-research JPM --capital 50000       # Vốn đầu tư $50K (default $33K)
```

## Cấu trúc

```
us-equity-research/
├── SKILL.md                          # Orchestrator 7 phase (<500 dòng)
├── agents/openai.yaml                # CLI display
├── references/                       # Progressive disclosure
│   ├── ⭐ insight_frames.md          # 12 frames + archetype router (CORE)
│   ├── data_sources.md               # 10 source categories + yfinance script
│   ├── data_pitfalls.md              # 7 bẫy data US
│   ├── valuation_formulas.md         # P/E P/B 5Y/10Y, DCF, EV/EBITDA
│   ├── technical_methodology.md      # ACTIVE + PROFILE mode
│   ├── analyst_research.md           # sell-side + independent synthesis
│   ├── language_layers.md            # glossary + 💡 Nói cách khác
│   └── dashboard_design.md           # 22 section map, CSS, Chart.js
├── scripts/
│   └── ⭐ fetch_us_data.py           # yfinance data fetcher (13 sections, 3 giây)
└── assets/
    ├── README.md                     # Cách dùng template
    ├── ⭐ dashboard_skeleton.html    # Template sạch (54KB, 105 tokens)
    └── dashboard_example_orcl.html   # Reference example ORCL (depth benchmark)
```

## Pipeline 7 phase

| Phase | Việc |
|---|---|
| **0. Discovery** (interactive) | Confirm ticker/period/capital/deploy + auto-detect sector → propose insight frames → user confirm |
| **1. Data research** | yfinance script (primary) + 4 subagent WebFetch song song (SEC, Yahoo, Macrotrends, analyst) |
| **2. Insight engine** (dynamic) | Mỗi frame stress-test + "honest correction" BẮT BUỘC |
| **3. 19 generic sections** | Hero → exec → biz → industry → history → segment → thesis → valuation → peer → BS+FCF → risk → 33K → scenario → checklist |
| **4. Language layers** | Glossary 12+12 term + 💡 Nói cách khác callouts |
| **5. Dashboard render** | Fill skeleton template + TOC + xref auto-gen + quality gates |
| **6. Deploy Vercel** | `vercel deploy --prod -y` |

## 12 Insight Frames

| # | Frame | Khi nào trigger |
|---|---|---|
| 1 | Value-chain positioning | Công ty là mắt xích chuỗi giá trị hot (AI/EV/semis) |
| 2 | Margin defensibility / barriers | Biên thấp, capex-heavy |
| 3 | Contract / backlog moat | RPO/backlog là KPI headline |
| 4 | Counterparty / concentration risk | 1 khách lớn drive thesis |
| 5 | Regulatory / compliance moat | Healthcare, finance, govtech |
| 6 | Cyclicality / obsolescence analog | Capex boom, hype cycle |
| 7 | Capital allocation quality | Buyback/M&A/dividend phức tạp |
| 8 | Platform / ecosystem moat | Network effect (Apple, Visa) |
| 9 | Pricing power / brand premium | Premium brand (LVMH, Coca-Cola) |
| 10 | Secular tailwind / demographic | Mega-trend (aging, decarbon) |
| 11 | M&A / conglomerate discount | Multi-segment, sum-of-parts |
| 12 | Secular decline / disruption | Legacy industry disrupted |

## Yêu cầu

- **ZCode CLI** (để chạy skill)
- **Python 3.10+** + `pip install yfinance pandas` (cho data fetcher)
- **Node.js** (verify inline JS syntax)
- **Vercel CLI** (deploy, optional nếu `--no-deploy`)
- **Git** + **GitHub** (nếu muốn version control)

## Đã prove qua 2 báo cáo

| Ticker | Sector | Insight frames chạy | Deploy URL |
|---|---|---|---|
| **ORCL** | Software/Cloud | Value-chain AI + Barriers + Hardware supply | [orcl-deploy.vercel.app](https://orcl-deploy.vercel.app) |
| **MSFT** | Software/Cloud | OpenAI risk + Ecosystem + Capital alloc + Regulatory | [msft-deploy.vercel.app](https://msft-deploy.vercel.app) |

Cùng archetype (Software/Cloud) NHƯNG insight engine tạo ra **content hoàn toàn khác** — chứng minh tính "động" của skill.

## License

MIT — dùng tự do, attribution appreciated.

## Tác giả

Thanhtran-165 — ZCode Project 2026
