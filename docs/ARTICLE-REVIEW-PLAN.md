# 全站逐篇複審計畫（維護者）

本計畫用於**系統性把每一篇文章過一遍**：結構是否對、內容是否對、連結是否活、與 canonical 是否一致。

!!! note "與既有文件的關係"
    | 文件 | 用途 |
    |------|------|
    | [寫作規範](STYLE-GUIDE.md) | 怎麼寫、A 級標準 |
    | [頁面章節規範](PAGE-STRUCTURE-GUIDE.md) | 每頁應有哪些章節、應呈現什麼 |
    | [投資審查檢核表](INVESTMENT-REVIEW-CHECKLIST.md) | 內容對不對（五維 + P0～P3） |
    | [內容覆蓋矩陣](CONTENT-COVERAGE-MATRIX.md) | 等級與進度總覽 |
    | `reports/investment-review.md` | 複審發現與修正紀錄 |

**學員可略過本頁。**

---

## 一、目標與範圍

| 項目 | 說明 |
|------|------|
| **總篇數** | **136** 篇 Markdown（含維護者頁） |
| **學員正文** | **118** 篇（排除 8 維護規範 + 10 參考附錄中的純索引頁，依下方清單） |
| **完成定義** | 該篇勾選「結構 ✅ + 內容 ✅ + 連結 ✅」；若有修改則跑 CI 通過 |
| **建議節奏** | 每批 **8～12 篇** → 修正 → `pytest` + `check_links` → commit → 勾選 |

---

## 二、單篇複審流程（約 15～25 分鐘／篇）

每篇文章依序做：

### Step 1｜對類型（1 分鐘）

對照 [頁面章節規範 § 一](PAGE-STRUCTURE-GUIDE.md#一八種頁面類型與標準章節)，確認屬 A～H 哪一類。

### Step 2｜結構驗收（5 分鐘）

- [ ] H1、`## 本篇你會學到`（例外頁除外）
- [ ] 該類型**必備章節**齊全（看表要有手算、詞典要五表、案例要免責與反思）
- [ ] `## 重點回顧` + `相關` 連結
- [ ] 教學頁有 `## 自我檢查`（案例頁除外）
- [ ] 無簡體字；英文術語僅首次括註（詞典除外）

### Step 3｜內容驗收（10 分鐘）

對照 [投資審查檢核表](INVESTMENT-REVIEW-CHECKLIST.md) 的 A～E 區：

- [ ] **數字**：稅費、T+2、漲跌停、除息參考價、手算可重算
- [ ] **用語**：與詞典、canonical 一致
- [ ] **風險**：教學用、常見誤區、指標滯後／強勢股例外（技術面）
- [ ] **canonical**：未重複展開權威章節（見 [架構說明](ARCHITECTURE.md)）
- [ ] **案例**：結論含「非投資建議」

發現問題記 **P0～P3**；P0/P1 當批必修。

### Step 4｜連結與建置（改動後才做）

```bash
uv run pytest tests/ -q
uv run python scripts/check_links.py --strict
uv run mkdocs build --strict
```

### Step 5｜登記

- 在本頁下方對應列將 `狀態` 改為 `✅`
- 有投資內容爭議 → 寫入 `reports/investment-review.md`
- 等級變動 → 更新 [CONTENT-COVERAGE-MATRIX.md](CONTENT-COVERAGE-MATRIX.md)

---

## 三、建議複審順序（12 批）

**原則**：先 **canonical／高風險數字** → 入門制度 → 看表看圖 → 模式風控 → 案例收尾 → 附錄與維護者頁。

```mermaid
flowchart LR
    P0[批0 Canonical] --> P1[批1-2 入門]
    P1 --> P2[批3 看表]
    P2 --> P3[批4-5 看圖詞典]
    P3 --> P4[批6-8 分析模式風控]
    P4 --> P5[批9-10 老手人設案例]
    P5 --> P6[批11 附錄維護]
```

---

### 批 0｜Canonical 與高風險數字（8 篇）— 優先

| # | 頁面 | 類型 | 複審重點 | 狀態 |
|---|------|------|----------|------|
| 0-1 | [trading-costs](06-risk/trading-costs.md) | 教學 | 稅率、損益平衡、期望值手算 | ☐ |
| 0-2 | [taxes-for-costing](appendix/taxes-for-costing.md) | 教學 | 2.11% 健保、綜所稅邊界 | ☐ |
| 0-3 | [capital](06-risk/capital.md) | 教學 | 閒錢、認賠殺出、曝險 | ☐ |
| 0-4 | [settlement-fees](01-basics/settlement-fees.md) | 教學 | T+2、不重複稅表 | ☐ |
| 0-5 | [etf-costs-and-premium](01-basics/etf-costs-and-premium.md) | 教學 | 三層費用、折溢價手算 | ☐ |
| 0-6 | [etf-passive-dca](08-investing/etf-passive-dca.md) | 教學 | 0050 定額、閒錢 | ☐ |
| 0-7 | [dividend-investing](08-investing/dividend-investing.md) | 教學 | 存股框架 | ☐ |
| 0-8 | [margin-trading](06-risk/margin-trading.md) | 教學 | 維持率、追繳 | ☐ |

---

### 批 1｜入門專章（上）（9 篇）

| # | 頁面 | 類型 | 狀態 |
|---|------|------|------|
| 1-1 | [index](01-basics/index.md) | 樞紐 | ☐ |
| 1-2 | [what-is-stock](01-basics/what-is-stock.md) | 教學 | ☐ |
| 1-3 | [price-and-cap](01-basics/price-and-cap.md) | 教學 | ☐ |
| 1-4 | [quote-screen](01-basics/quote-screen.md) | 教學 | ☐ |
| 1-5 | [market-overview](01-basics/market-overview.md) | 教學 | ☐ |
| 1-6 | [trading-restrictions](01-basics/trading-restrictions.md) | 教學 | ☐ |
| 1-7 | [trading-flow](01-basics/trading-flow.md) | 教學 | ☐ |
| 1-8 | [first-trade-walkthrough](01-basics/first-trade-walkthrough.md) | 教學 | ☐ |
| 1-9 | [open-account](01-basics/open-account.md) | 教學 | ☐ |

---

### 批 2｜入門專章（下）（8 篇）

| # | 頁面 | 類型 | 狀態 |
|---|------|------|------|
| 2-1 | [roles](01-basics/roles.md) | 教學 | ☐ |
| 2-2 | [ipo-subscription](01-basics/ipo-subscription.md) | 教學 | ☐ |
| 2-3 | [dividend](01-basics/dividend.md) | 教學 | ☐ |
| 2-4 | [etf-intro](01-basics/etf-intro.md) | 教學 | ☐ |
| 2-5 | [mutual-fund-intro](01-basics/mutual-fund-intro.md) | 教學 | ☐ |
| 2-6 | [futures-intro](01-basics/futures-intro.md) | 教學 | ☐ |
| 2-7 | [index](index.md) | 首頁 | ☐ |
| 2-8 | [data-sources](appendix/data-sources.md) | 教學 | ☐ |

---

### 批 3｜怎麼看表（11 篇）

| # | 頁面 | 類型 | 狀態 |
|---|------|------|------|
| 3-1 | [index](03-tables/index.md) | 樞紐 | ☐ |
| 3-2 | [watchlist](03-tables/watchlist.md) | 看表 | ☐ |
| 3-3 | [deep-dive-tabs](03-tables/deep-dive-tabs.md) | 看表 | ☐ |
| 3-4 | [revenue](03-tables/revenue.md) | 看表 | ☐ |
| 3-5 | [institutional](03-tables/institutional.md) | 看表 | ☐ |
| 3-6 | [margin](03-tables/margin.md) | 看表 | ☐ |
| 3-7 | [valuation](03-tables/valuation.md) | 看表 | ☐ |
| 3-8 | [financials](03-tables/financials.md) | 看表 | ☐ |
| 3-9 | [scoring](03-tables/scoring.md) | 看表 | ☐ |
| 3-10 | [dividend-schedule](03-tables/dividend-schedule.md) | 看表 | ☐ |
| 3-11 | [block-trade](03-tables/block-trade.md) | 看表 | ☐ |

---

### 批 4｜怎麼看圖（上）（9 篇）

| # | 頁面 | 類型 | 狀態 |
|---|------|------|------|
| 4-1 | [index](04-charts/index.md) | 樞紐 | ☐ |
| 4-2 | [line-charts](04-charts/line-charts.md) | 教學 | ☐ |
| 4-3 | [intraday-charts](04-charts/intraday-charts.md) | 教學 | ☐ |
| 4-4 | [kline-basics](04-charts/kline-basics.md) | 教學 | ☐ |
| 4-5 | [kline-reading](04-charts/kline-reading.md) | 教學 | ☐ |
| 4-6 | [candle-patterns](04-charts/candle-patterns.md) | 教學 | ☐ |
| 4-7 | [candle-quickref](04-charts/candle-quickref.md) | 速查 | ☐ |
| 4-8 | [candle-combinations](04-charts/candle-combinations.md) | 教學 | ☐ |
| 4-9 | [volume-price](04-charts/volume-price.md) | 教學 | ☐ |

---

### 批 5｜怎麼看圖（下）＋詞典（上）（10 篇）

| # | 頁面 | 類型 | 狀態 |
|---|------|------|------|
| 5-1 | [chips-charts](04-charts/chips-charts.md) | 教學 | ☐ |
| 5-2 | [fundamental-charts](04-charts/fundamental-charts.md) | 教學 | ☐ |
| 5-3 | [market-charts](04-charts/market-charts.md) | 教學 | ☐ |
| 5-4 | [indicator-quickref](04-charts/indicator-quickref.md) | 速查 | ☐ |
| 5-5 | [ma](04-charts/ma.md) | 教學 | ☐ |
| 5-6 | [macd](04-charts/macd.md) | 教學 | ☐ |
| 5-7 | [rsi](04-charts/rsi.md) | 教學 | ☐ |
| 5-8 | [kd](04-charts/kd.md) | 教學 | ☐ |
| 5-9 | [bollinger](04-charts/bollinger.md) | 教學 | ☐ |
| 5-10 | [index](02-glossary/index.md) | 樞紐 | ☐ |

---

### 批 6｜詞典（11 篇）

| # | 頁面 | 類型 | 狀態 |
|---|------|------|------|
| 6-1 | [dictionary](02-glossary/dictionary.md) | 索引 | ☐ |
| 6-2 | [quotes](02-glossary/quotes.md) | 詞典 | ☐ |
| 6-3 | [trading-terms](02-glossary/trading-terms.md) | 詞典 | ☐ |
| 6-4 | [pnl](02-glossary/pnl.md) | 詞典 | ☐ |
| 6-5 | [position](02-glossary/position.md) | 詞典 | ☐ |
| 6-6 | [chips](02-glossary/chips.md) | 詞典 | ☐ |
| 6-7 | [fundamentals](02-glossary/fundamentals.md) | 詞典 | ☐ |
| 6-8 | [technical](02-glossary/technical.md) | 詞典 | ☐ |
| 6-9 | [market-terms](02-glossary/market-terms.md) | 詞典 | ☐ |
| 6-10 | [macro](02-glossary/macro.md) | 詞典 | ☐ |
| 6-11 | [risk](02-glossary/risk.md) | 詞典 | ☐ |

詞典批完成後：確認 `dictionary.md` 每列「詳見」錨點有效。

---

### 批 7｜分析思維（7 篇）

| # | 頁面 | 類型 | 狀態 |
|---|------|------|------|
| 7-1 | [index](05-analysis/index.md) | 樞紐 | ☐ |
| 7-2 | [three-pillars](05-analysis/three-pillars.md) | 教學 | ☐ |
| 7-3 | [fundamental-framework](05-analysis/fundamental-framework.md) | 教學 | ☐ |
| 7-4 | [timeframes](05-analysis/timeframes.md) | 教學 | ☐ |
| 7-5 | [conference](05-analysis/conference.md) | 教學 | ☐ |
| 7-6 | [cross-market](05-analysis/cross-market.md) | 教學 | ☐ |
| 7-7 | [active-etf](05-analysis/active-etf.md) | 教學 | ☐ |

---

### 批 8｜投資模式（15 篇）

| # | 頁面 | 類型 | 狀態 |
|---|------|------|------|
| 8-1 | [index](08-investing/index.md) | 樞紐 | ☐ |
| 8-2 | [choose-style](08-investing/choose-style.md) | 教學 | ☐ |
| 8-3 | [mode-psychology](08-investing/mode-psychology.md) | 教學 | ☐ |
| 8-4 | [day-trade](08-investing/day-trade.md) | 教學 | ☐ |
| 8-5 | [overnight](08-investing/overnight.md) | 教學 | ☐ |
| 8-6 | [swing-short](08-investing/swing-short.md) | 教學 | ☐ |
| 8-7 | [swing-mid](08-investing/swing-mid.md) | 教學 | ☐ |
| 8-8 | [long-term](08-investing/long-term.md) | 教學 | ☐ |
| 8-9 | [dividend-strategies](08-investing/dividend-strategies.md) | 教學 | ☐ |
| 8-10 | [etf-investing](08-investing/etf-investing.md) | 教學 | ☐ |
| 8-11 | [etf-high-dividend](08-investing/etf-high-dividend.md) | 教學 | ☐ |
| 8-12 | [investment-linked-policy](08-investing/investment-linked-policy.md) | 教學 | ☐ |
| 8-13 | [insurance-fx-products](08-investing/insurance-fx-products.md) | 教學 | ☐ |
| 8-14 | *(批 0 已含 etf-passive-dca、dividend-investing)* | — | — |
| 8-15 | 交叉檢查：模式頁與 [10-persona](10-persona/index.md) 建議一致 | — | ☐ |

---

### 批 9｜風控與紀律（6 篇）

| # | 頁面 | 類型 | 狀態 |
|---|------|------|------|
| 9-1 | [index](06-risk/index.md) | 樞紐 | ☐ |
| 9-2 | [stop-loss](06-risk/stop-loss.md) | 教學 | ☐ |
| 9-3 | [discipline](06-risk/discipline.md) | 教學 | ☐ |
| 9-4 | [emergency-playbook](06-risk/emergency-playbook.md) | 教學 | ☐ |
| 9-5 | *(批 0 已含 capital、trading-costs、margin-trading)* | — | — |
| 9-6 | 全章交叉：停損數字與 [stop-loss](06-risk/stop-loss.md) A/B/C 層一致 | — | ☐ |

---

### 批 10｜老手專區＋人設（14 篇）

| # | 頁面 | 類型 | 狀態 |
|---|------|------|------|
| 10-1 | [index](09-advanced/index.md) | 樞紐 | ☐ |
| 10-2 | [research-workflow](09-advanced/research-workflow.md) | 教學 | ☐ |
| 10-3 | [multi-timeframe](09-advanced/multi-timeframe.md) | 教學 | ☐ |
| 10-4 | [portfolio](09-advanced/portfolio.md) | 教學 | ☐ |
| 10-5 | [macro-rotation](09-advanced/macro-rotation.md) | 教學 | ☐ |
| 10-6 | [advanced-chips](09-advanced/advanced-chips.md) | 教學 | ☐ |
| 10-7 | [event-playbook](09-advanced/event-playbook.md) | 教學 | ☐ |
| 10-8 | [futures-signal](09-advanced/futures-signal.md) | 教學 | ☐ |
| 10-9 | [veteran-pitfalls](09-advanced/veteran-pitfalls.md) | 教學 | ☐ |
| 10-10 | [index](10-persona/index.md) | 人設 | ☐ |
| 10-11 | [beginner](10-persona/beginner.md) | 人設 | ☐ |
| 10-12 | [busy](10-persona/busy.md) | 人設 | ☐ |
| 10-13 | [active](10-persona/active.md) | 人設 | ☐ |
| 10-14 | [steady](10-persona/steady.md) | 人設 | ☐ |

---

### 批 11｜實戰案例（17 篇）

| # | 頁面 | 主題群 | 狀態 |
|---|------|--------|------|
| 11-1 | [index](07-cases/index.md) | 導覽 | ☐ |
| 11-2 | [revenue-turn](07-cases/revenue-turn.md) | 營收 | ☐ |
| 11-3 | [hammer-ma](07-cases/hammer-ma.md) | 技術 | ☐ |
| 11-4 | [institutional-flow](07-cases/institutional-flow.md) | 籌碼 | ☐ |
| 11-5 | [day-trade-risk](07-cases/day-trade-risk.md) | 當沖 | ☐ |
| 11-6 | [valuation-trap](07-cases/valuation-trap.md) | 估值 | ☐ |
| 11-7 | [macd-divergence](07-cases/macd-divergence.md) | 技術 | ☐ |
| 11-8 | [conference-chips](07-cases/conference-chips.md) | 籌碼 | ☐ |
| 11-9 | [gap-breakout](07-cases/gap-breakout.md) | 技術 | ☐ |
| 11-10 | [short-squeeze](07-cases/short-squeeze.md) | 籌碼 | ☐ |
| 11-11 | [dividend-play](07-cases/dividend-play.md) | 除息 | ☐ |
| 11-12 | [etf-dca-drawdown](07-cases/etf-dca-drawdown.md) | ETF | ☐ |
| 11-13 | [fund-policy-faq](07-cases/fund-policy-faq.md) | 理財 | ☐ |
| 11-14 | [macro-rates](07-cases/macro-rates.md) | 總經 | ☐ |
| 11-15 | [odd-lot-mistake](07-cases/odd-lot-mistake.md) | 小資 | ☐ |
| 11-16 | [ex-dividend-mistake](07-cases/ex-dividend-mistake.md) | 除息 | ☐ |
| 11-17 | [disposal-stock-trap](07-cases/disposal-stock-trap.md) | 限制 | ☐ |

案例批：逐篇確認 SVG 存在、手算數字與正文一致。

---

### 批 12｜附錄與維護者頁（14 篇）

| # | 頁面 | 類型 | 狀態 |
|---|------|------|------|
| 12-1 | [formulas](appendix/formulas.md) | 教學 | ☐ |
| 12-2 | [investor-checklist](appendix/investor-checklist.md) | 教學 | ☐ |
| 12-3 | [faq](appendix/faq.md) | 教學 | ☐ |
| 12-4 | [abbreviations](appendix/abbreviations.md) | 參考 | ☐ |
| 12-5 | [reference-book](appendix/reference-book.md) | 參考 | ☐ |
| 12-6 | [video-resources](appendix/video-resources.md) | 參考 | ☐ |
| 12-7 | [stock-tool-map](appendix/stock-tool-map.md) | 參考 | ☐ |
| 12-8 | [dev-glossary](appendix/dev-glossary.md) | 參考 | ☐ |
| 12-9 | [disclaimer](appendix/disclaimer.md) | 法務 | ☐ |
| 12-10 | [STYLE-GUIDE](STYLE-GUIDE.md) | 維護 | ☐ |
| 12-11 | [PAGE-STRUCTURE-GUIDE](PAGE-STRUCTURE-GUIDE.md) | 維護 | ☐ |
| 12-12 | [CONTENT-COVERAGE-MATRIX](CONTENT-COVERAGE-MATRIX.md) | 維護 | ☐ |
| 12-13 | [CHART-CHECKLIST](CHART-CHECKLIST.md) | 維護 | ☐ |
| 12-14 | [INVESTMENT-REVIEW-CHECKLIST](INVESTMENT-REVIEW-CHECKLIST.md) | 維護 | ☐ |
| 12-15 | [ARCHITECTURE](ARCHITECTURE.md) | 維護 | ☐ |

---

## 四、每批交付檢查清單

完成一批後勾選：

- [ ] 該批所有頁面 `狀態` 已改 `✅`
- [ ] P0/P1 已修正或記錄於 `reports/investment-review.md`
- [ ] `uv run pytest tests/ -q` 通過
- [ ] `uv run python scripts/check_links.py --strict` ERROR=0
- [ ] `uv run mkdocs build --strict` 成功
- [ ] Git commit（一批一 commit，訊息註明批號）
- [ ] [CONTENT-COVERAGE-MATRIX](CONTENT-COVERAGE-MATRIX.md) 有變動則更新

---

## 五、進度總覽（手動更新）

| 批次 | 篇數 | 完成 | 完成日 |
|------|------|------|--------|
| 批 0 Canonical | 8 | 0/8 | |
| 批 1 入門上 | 9 | 0/9 | |
| 批 2 入門下 | 8 | 0/8 | |
| 批 3 看表 | 11 | 0/11 | |
| 批 4 看圖上 | 9 | 0/9 | |
| 批 5 看圖下+詞典入 | 10 | 0/10 | |
| 批 6 詞典 | 11 | 0/11 | |
| 批 7 分析 | 7 | 0/7 | |
| 批 8 模式 | 13* | 0/13 | |
| 批 9 風控 | 4* | 0/4 | |
| 批 10 老手+人設 | 14 | 0/14 | |
| 批 11 案例 | 17 | 0/17 | |
| 批 12 附錄維護 | 15 | 0/15 | |
| **合計** | **136** | **0/136** | |

\*批 8、9 含與批 0 交叉檢查項，不重複計入 canonical 篇數。

---

## 六、建議時程（參考）

| 節奏 | 預估 |
|------|------|
| 每週 2 批（約 20 篇） | 全站約 **6～7 週** |
| 每週 1 批 | 全站約 **12 週** |
| 僅複審無修改 | 每篇約 10 分鐘；有修改則加測試時間 |

---

## 七、與 AI 協作建議

若使用 Cursor／AI 代為複審，每次 prompt 建議格式：

```
請執行 ARTICLE-REVIEW-PLAN 批 N：
1. 依 PAGE-STRUCTURE-GUIDE 檢查結構
2. 依 INVESTMENT-REVIEW-CHECKLIST 檢查內容
3. 列出 P0～P3 發現；P0/P1 直接修正
4. 跑 pytest + check_links + mkdocs build
5. 更新本計畫狀態欄與 investment-review.md
6. commit：review: 🔍 [AI] 完成批 N 逐篇複審
```

---

## 重點回顧

- **136 篇**、**12 批**；先 canonical 再入門，最後案例與附錄。
- 每篇走 **類型 → 結構 → 內容 → 連結 → 登記** 五步。
- 進度以本頁 `狀態` 欄與第五節總表追蹤。

相關：[頁面章節規範](PAGE-STRUCTURE-GUIDE.md) · [投資審查檢核表](INVESTMENT-REVIEW-CHECKLIST.md) · [內容覆蓋矩陣](CONTENT-COVERAGE-MATRIX.md)
