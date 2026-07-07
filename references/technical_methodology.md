# Technical Methodology — Port từ vn-technical-analysis cho US stock

> 2 mode TÁCH BIỆT (KHÔNG trộn ngôn ngữ). Đọc ở Phase 3 Section 18 (ACTIVE) + Section 19 (PROFILE).

## A. Data source — Yahoo Finance Chart API

```
Weekly 52 tuần:
  https://query2.finance.yahoo.com/v8/finance/chart/{TICKER}?range=1y&interval=1wk

Daily ~2 năm (~500 phiên):
  https://query2.finance.yahoo.com/v8/finance/chart/{TICKER}?range=2y&interval=1d

Index benchmark (^GSPC S&P 500, ^IXIC Nasdaq, ^DJI Dow):
  https://query2.finance.yahoo.com/v8/finance/chart/^GSPC?range=1y&interval=1wk
```

Returns JSON: `timestamp[]`, `indicators.quote[0]` {open, high, low, close, volume}, `indicators.adjclose[0]`. Adjusted for splits + dividends.

**Cross-check**: stockanalysis.com, macrotrends for OHLCV confirmation.

## B. Mode ACTIVE — timing/verdict (Section 18)

### Indicators (tính từ weekly 52w + daily)
| Indicator | Công thức | Khi nào quan trọng |
|---|---|---|
| **MA10/MA20/MA50** | Trung bình động closing prices | Xu hướng ngắn/trung hạn |
| **RSI(14)** Wilder | 100 - 100/(1+RS), RS = avg gain/avg loss | <30 oversold, >70 overbought |
| **MACD(12,26,9)** | EMA12 - EMA26, Signal = EMA9 của MACD | Bullish/bearish crossover |
| **Bollinger Bands(20, 2σ)** | MA20 ± 2× standard deviation | Overbought/oversold + breakout |
| **Beta** | Cov(stock,market)/Var(market) vs ^GSPC | Độ rủi ro vs thị trường |
| **Correlation** | Pearson(stock, index) | Mức độ liên quan thị trường |

### 6 Signals → Tech Score (−6 → +6)

| Signal | +1 (bullish) | -1 (bearish) |
|---|---|---|
| Giá vs MA10 | Trên | Dưới |
| Giá vs MA20 | Trên | Dưới |
| Giá vs MA50 | Trên | Dưới |
| RSI | > 55 | < 45 |
| MACD vs Signal | Trên (bullish) | Dưới (bearish) |
| BB Position (% trong band) | > 50% | < 50% |

### Verdict mapping
| Score | Verdict (TECHNICAL only — KHÔNG phải khuyến nghị giao dịch) |
|---|---|
| +4 đến +6 | TECHNICAL STRONG BULLISH |
| +1 đến +3 | TECHNICAL BULLISH |
| -1 đến 0 | TECHNICAL NEUTRAL |
| -3 đến -2 | TECHNICAL BEARISH |
| -6 đến -4 | TECHNICAL STRONG BEARISH |

**⚠️ GUARDRAIL BẮT BUỘC** (học từ review 7/2026):
- **KHÔNG dùng "STRONG BUY/BUY/SELL/STRONG SELL"** — đó là khuyến nghị giao dịch, technical alone không đủ.
- Dùng "TECHNICAL STRONG BULLISH/BEARISH" — mô tả trạng thái kỹ thuật, không phải lệnh.
- **Verdict technical phải kết hợp fundamental**: "Tech Score +5 NHƯNG valuation Danger Zone → KHÔNG kết luận bullish cho đầu tư 3-5 năm."
- **Score bearish không tự động = "bán"**: Case ORCL Tech Score −5 NHƯNG oversold + support zone → có thể accumulation zone cho value investor.
- Technical = 1 input, không phải verdict cuối. Final verdict = fundamental + valuation + technical.

### Patterns detection (CHỈ khi có evidence)
- **Double Bottom/Top**: 2 đáy/đỉnh cách ≥5 tuần, chênh <3%
- **Ascending/Descending Channel**: fit trendline qua swing highs/lows
- **Candlestick**: Hammer, Marubozu, Doji, Engulfing — flag từng nến với điều kiện body/wick
- **Divergence**: check 2 đáy giá + 2 đáy RSI — CHỈ flag nếu giá giảm + RSI tăng (bullish) hoặc ngược

**Anti-pattern**: KHÔNG claim pattern nếu data không show — nói "không có pattern detectable".

### Trading Strategy 3 scenarios (tích cực / trung tính / tiêu cực)
- **Tích cực**: điều kiện breakout → target → stop-loss
- **Trung tính**: range-bound, chờ confirm
- **Tiêu cực**: điều kiện breakdown → next support → cut loss

## C. Mode PROFILE — hồ sơ giá-khối lượng (Section 19) NON-ADVICE

### Ngôn ngữ: `neutral_descriptive_non_advice`
**Bắt buộc**:
- KHÔNG dùng "bullish/bearish/strong buy/strong sell/khuyến nghị mua/khuyến nghị bán/tín hiệu vào/tín hiệu ra"
- Dùng "đang tăng/đang giảm/quan sát/hành vi lịch sử/thấy rằng"
- Mỗi metric kèm `interpretation_guardrail`

**Verify bắt buộc** trước khi hoàn tất:
```bash
# Extract section PROFILE ra, check forbidden words
grep -iE "bullish|bearish|strong buy|khuyến nghị mua|khuyến nghị bán|tín hiệu vào|tín hiệu ra" {output}.html | grep -v "<script>"
# Phải rỗng
```

### 15 blocks profile (subset, daily ~500 phiên)
1. **price_behavior**: return 1M/3M/1Y/2Y, % from 52w high/low
2. **volatility**: HV10/20/60/120/252 annualized (log returns × √252)
3. **drawdown**: max drawdown, current drawdown from peak, underwater curve
4. **liquidity**: avg volume, dollar volume, spread proxy
5. **return_distribution**: histogram, skewness, kurtosis
6. **tail_risk**: VaR (95%/99%), Expected Shortfall (CVaR) — historical
7. **liquidity_risk**: days-to-exit at avg volume
8. **volume_price**: average volume up-days vs down-days
9. **VPCI**: Volume Price Confirmation Indicator (Wyckoff-inspired)
10. **money_flow**: OBV, VPT, CMF (Chaikin Money Flow 20d)
11. **effort_result**: Wyckoff effort vs result (volume vs price range)
12. **high_volume_behavior**: event study on high-volume days
13. **PVI/NVI**: Positive/Negative Volume Index
14. **volume_at_price (VAP)**: POC (Point of Control), value areas
15. **regime**: trending vs mean-reverting (Hurst exponent or simple rule)

### Setup heuristic + archetype (8 setups)
- triangles ascending/descending
- double bottom/top
- support breakout
- oversold reversal
- channel continuation
- accumulation breakout
- trap (fake breakout)
- momentum exhaustion

**Archetype 4 loại** (scoring 0-100):
- **trend_following**: clear directional, momentum-confirmed
- **accumulation_breakout**: base then breakout with volume
- **trap_prone**: many fakeouts (case ORCL: bounce to $250 then collapse)
- **mixed**: no clear pattern

### Non-conclusion panel (BẮT BUỘC cuối section)
4 điểm, ít nhất điểm 1+2 bắt buộc:
1. "Section này là hồ sơ hành vi lịch sử — không phải khuyến nghị hoặc lời gọi giao dịch."
2. "Tỷ lệ/pattern trong quá khứ không đảm bảo lặp lại trong tương lai."
3. Cụ thể cho stock (regime observation, key concern)
4. Reminder kết hợp fundamental + valuation trước khi quyết định

## D. Sub-skills coordination

Port từ `vn-technical-analysis` skill methodology. Tham khảo:
- `~/.zcode/skills/vn-technical-analysis/references/indicators.md` — code Node.js/Python MA/RSI/MACD/BB/Beta
- `~/.zcode/skills/vn-technical-analysis/references/pattern_detection.md` — code detection
- `~/.zcode/skills/vn-technical-analysis/references/stock_profile_blocks.md` — 15 block Python (portable)
- `~/.zcode/skills/vn-technical-analysis/references/pattern_scoring.md` — 8 setups + archetype
- `~/.zcode/skills/vn-technical-analysis/references/metric_guardrails.md` — forbidden list + glossary

Sự khác biệt duy nhất: data source (Yahoo Finance thay vì vnstock). Methodology 100% portable.
