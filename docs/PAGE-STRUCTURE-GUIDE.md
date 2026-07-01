# 全站頁面章節與內容規範（維護者）

本頁說明 Stock School **每一類頁面應有哪些章節**，以及**各章節應呈現什麼內容**。撰寫依據見 [寫作規範](STYLE-GUIDE.md)；canonical 對照見 [架構說明](ARCHITECTURE.md)。

!!! note "怎麼用"
    - **新增頁面**：先對照下方「頁面類型」，套用對應骨架。
    - **潤稿驗收**：確認章節齊全、內容職責不與 canonical 章節重複。
    - **學員可略過**本頁。

---

## 一、八種頁面類型與標準章節

### 類型 A｜通用教學頁

**適用**：入門、投資模式、風控、分析、老手專區、多數 04-charts 專題頁。

| 章節 | 必備 | 應呈現內容 |
|------|:----:|------------|
| `# 標題` | ✅ | 主題名稱；可含英文括註（首次） |
| `## 本篇你會學到` | ✅ | 3～5 條可驗收學習目標 |
| 正文 `## …` | ✅ | 概念、表格、mermaid、admonition；**白話 + 連結 canonical** |
| `## 常見誤區` | 視主題 | 誤區｜正確做法 對照表（canonical 頁必備） |
| `## 自我檢查` | ✅* | 3 題（概念／判斷／情境）+ 摺疊參考答案；*有對應案例者可改導向案例 |
| `## 重點回顧` | ✅ | 2～4 條收斂要點 |
| `相關` 連結列 | ✅ | 站內相對路徑，指向專章／案例／詞典 |

**語氣**：教學用、非投資建議；不報明牌。

---

### 類型 B｜看表頁（`03-tables/*.md`，index 除外）

| 章節 | 必備 | 應呈現內容 |
|------|:----:|------------|
| `## 本篇你會學到` | ✅ | 讀這張表能回答什麼問題 |
| `## 示意表` | ✅ | 教學用合成數據；標明非即時行情 |
| `## 欄位解讀` | ✅ | 欄位｜意義｜怎麼用 |
| `## 在哪裡看到` | ✅ | MOPS／券商分頁；連 [資料來源](appendix/data-sources.md) |
| `## 手算一例` 或 `## 導覽練習一例` | ✅ | 用示意表一列把公式算給讀者看 |
| `## 閱讀步驟` | ✅ | 編號步驟 + 可選 mermaid |
| `## 常見誤區` | ✅ | 看表時典型誤判 |
| `## 讀完請做` | ✅ | 導向對應案例或自檢 |
| `## 重點回顧` + 相關 | ✅ | — |

**驗收**：`tests/test_table_coverage.py` 自動把關。

---

### 類型 C｜詞典分類頁（`02-glossary/*.md`，index／dictionary 除外）

| 章節 | 必備 | 應呈現內容 |
|------|:----:|------------|
| `## 本篇你會學到` | ✅ | 本分類涵蓋哪些術語場景 |
| 每個 `## 詞條（English） {#錨點}` | ✅ | **五列表格**：英文｜定義｜在哪裡看到｜常見誤解｜小例子 |
| `## 自我檢查` | ✅ | 3 題，檢驗是否理解本分類核心詞 |
| `## 重點回顧` + 相關 | ✅ | — |

**錨點 ID 凍結**；`dictionary.md` 四欄索引必須同步。

---

### 類型 D｜案例頁（`07-cases/*.md`，index 除外）

| 章節 | 必備 | 應呈現內容 |
|------|:----:|------------|
| `## 本篇你會學到` | ✅ | 本案例要練什麼推理能力 |
| `!!! warning 免責聲明` | ✅ | 教學用、非投資建議 |
| `## 背景` | ✅ | 匿名情境設定 |
| `## 看到的資料` 或 `看到的表／圖` | ✅ | 表格或 SVG 示意 |
| `## 推理步驟` | ✅ | 編號邏輯 + 可選 mermaid |
| `## 結論（教學用）` | ✅ | 不暗示買賣信號 |
| `## 反思` | ✅ | 誤區｜修正 |
| `## 重點回顧` + 相關 | ✅ | 連回對應專章 |

**不需** `## 自我檢查`（案例本身即練習）。

---

### 類型 E｜專章樞紐 index

**適用**：`01-basics/index`、`02-glossary/index`、`03-tables/index`、`04-charts/index`、`05-analysis/index`、`06-risk/index`、`07-cases/index`、`08-investing/index`、`09-advanced/index`。

| 章節 | 必備 | 應呈現內容 |
|------|:----:|------------|
| `## 本篇你會學到` | ✅ | 本章在全站的定位 |
| 分類表／地圖／流程圖 | ✅ | 子頁清單 + 各頁一句話 |
| 建議閱讀順序 | 建議 | mermaid 或編號路徑 |
| `## 自我檢查` | ✅ | 3 題，檢驗是否理解本章導覽邏輯 |
| `## 重點回顧` + 相關 | ✅ | 指向首頁或相鄰專章 |

**不重複**子頁完整教學，只摘要 + 連結。

---

### 類型 F｜人設頁（`10-persona/`）

| 頁面 | 章節 | 應呈現內容 |
|------|------|------------|
| `index.md` | 身分對照表、mermaid、找到格子之後、自檢 | 12 型身分 → 建議模式 → 必讀專章 |
| `beginner`／`busy`／`active`／`steady` | 各 3 個 `### 身分` 小節 | 你是這型如果…｜建議主模式｜不建議｜第一步｜心態 |
| 分頁尾 | `## 自我檢查` + 相關 | 3 題對應該頁三種身分 |

---

### 類型 G｜速查頁（C 級定位）

**適用**：`indicator-quickref.md`、`candle-quickref.md`。

| 章節 | 應呈現內容 |
|------|------------|
| 指標／型態對照表 | 一頁查閱，連結完整教學頁 |
| `## 自我檢查` | 精簡 3 題 |
| `## 重點回顧` | 提醒「速查 ≠ 完整教學」 |

---

### 類型 H｜參考／維護者頁

| 頁面 | 章節職責 |
|------|----------|
| `index.md`（首頁） | 學習路徑、專章入口、模式捷徑；**不用**通用教學模板 |
| `dictionary.md` | 四欄詞條總表索引 |
| `abbreviations.md` | 縮寫對照 |
| `reference-book.md` | 基本資料書式欄位 |
| `video-resources.md` | 影片 → 本站章節對照 |
| `stock-tool-map.md` | 第三方工具 ↔ 本站章節 |
| `dev-glossary.md` | 學員詞 ↔ 程式用語 |
| `disclaimer.md` | 法務免責 |
| `STYLE-GUIDE`／`ARCHITECTURE`／`CONTENT-COVERAGE-MATRIX` 等 | 維護規範與進度 |

---

## 二、逐專章頁面清單

以下「應有章節」= 類型標準章節 + **該頁專屬正文**（`##` 小節主題）。

### 入門 `01-basics/`

| 頁面 | 類型 | 專屬正文應呈現 | 標準尾段 |
|------|------|----------------|----------|
| [index](01-basics/index.md) | 樞紐 | 三條主線、建議閱讀順序、與他章關係 | 重點回顧（無自檢） |
| [what-is-stock](01-basics/what-is-stock.md) | 教學 | 定義、股東權益、普通股、公司債比較、常見商品類型 | 常見誤區、自檢 |
| [price-and-cap](01-basics/price-and-cap.md) | 教學 | 股價≠貴便宜、市值、量價關係 | 自檢 |
| [quote-screen](01-basics/quote-screen.md) | 教學 | 五檔、內外盤、個股 vs ETF 報價差異、示意圖 | 自檢 |
| [market-overview](01-basics/market-overview.md) | 教學 | 上市櫃興櫃、交易時段、當沖、注意處置股 | 自檢 |
| [trading-restrictions](01-basics/trading-restrictions.md) | 教學 | 注意股、處置、全額交割、下單前檢查 | 自檢 |
| [trading-flow](01-basics/trading-flow.md) | 教學 | 下單類型、零股、T+2、交割戶 | 自檢 |
| [settlement-fees](01-basics/settlement-fees.md) | 教學 | T+2 時點、扣款順序；稅費**連結** canonical `trading-costs` | 自檢 |
| [first-trade-walkthrough](01-basics/first-trade-walkthrough.md) | 教學 | 全流程步驟、檢查清單 | 自檢 |
| [roles](01-basics/roles.md) | 教學 | 股東、券商、三大法人、ETF 角色 | 自檢 |
| [open-account](01-basics/open-account.md) | 教學 | 開戶流程、現股／當沖／信用資格 | 自檢 |
| [ipo-subscription](01-basics/ipo-subscription.md) | 教學 | 抽籤機制、預扣款、非穩賺 | 自檢 |
| [dividend](01-basics/dividend.md) | 教學 | 除權息、填息、殖利率 | 自檢 |
| [etf-intro](01-basics/etf-intro.md) | 教學 | ETF 概念、0050；個股 vs ETF **摘要** | 常見誤區、自檢 |
| [etf-costs-and-premium](01-basics/etf-costs-and-premium.md) | **canonical** | 三層費用、折溢價、收益平準金、手算複利 | 自檢 |
| [mutual-fund-intro](01-basics/mutual-fund-intro.md) | **canonical** | 基金 vs ETF vs 個股、內扣外扣、保單費用差 | 自檢 |
| [futures-intro](01-basics/futures-intro.md) | 教學 | 大小微台、保證金、散戶輔助判斷（不教炒期貨） | 自檢 |

---

### 術語詞典 `02-glossary/`

| 頁面 | 類型 | 本分類應涵蓋的術語領域 |
|------|------|------------------------|
| [index](02-glossary/index.md) | 樞紐 | 分類導覽、怎麼讀術語、影片對照 |
| [dictionary](02-glossary/dictionary.md) | 索引 | 全站四欄詞條總表 |
| [quotes](02-glossary/quotes.md) | 詞典 | OHLC、漲跌幅、五檔、漲跌停、前高前低 |
| [trading-terms](02-glossary/trading-terms.md) | 詞典 | 開平倉、回檔反彈、追高殺低、回測兩義 |
| [pnl](02-glossary/pnl.md) | 詞典 | 毛價差、淨利、停損停利、移動停利、損益兩平 |
| [position](02-glossary/position.md) | 詞典 | 張、持倉、當沖、做多做空 |
| [chips](02-glossary/chips.md) | 詞典 | 三大法人、融資融券、券資比、集保、分點 |
| [fundamentals](02-glossary/fundamentals.md) | 詞典 | PER、PBR、EPS、三率、MoM/YoY、ROE、護城河、DCF |
| [technical](02-glossary/technical.md) | 詞典 | MA、MACD、RSI、KD、支撐壓力、黃金死亡交叉 |
| [market-terms](02-glossary/market-terms.md) | 詞典 | 跳空、軋空、填息、洗盤、量價背離、Priced In |
| [macro](02-glossary/macro.md) | 詞典 | 升息降息、CPI/GDP、國債、QE、VIX、選擇權（邊界） |
| [risk](02-glossary/risk.md) | 詞典 | 曝險、最大回撤、風險報酬比、緊急停機 |

每詞典頁尾：**自我檢查** + **重點回顧**。

---

### 怎麼看表 `03-tables/`

| 頁面 | 專屬正文焦點 |
|------|--------------|
| [index](03-tables/index.md) | 十表分類、閱讀順序、依模式選表 |
| [watchlist](03-tables/watchlist.md) | 個股快照欄位、漲跌幅手算 |
| [deep-dive-tabs](03-tables/deep-dive-tabs.md) | 券商分頁地圖；**導覽練習**取代單欄手算 |
| [revenue](03-tables/revenue.md) | 月營收 MoM/YoY 手算 |
| [institutional](03-tables/institutional.md) | 法人合計、T+1 lag |
| [margin](03-tables/margin.md) | 券資比手算 |
| [valuation](03-tables/valuation.md) | PER/PBR/殖利率手算、官方防呆 |
| [financials](03-tables/financials.md) | 三率、淨利率手算 |
| [scoring](03-tables/scoring.md) | 多因子分差、四時間框架 |
| [dividend-schedule](03-tables/dividend-schedule.md) | 除息日程、殖利率反推 |
| [block-trade](03-tables/block-trade.md) | 鉅額金額手算 |

全部套用**類型 B** 看表骨架。

---

### 怎麼看圖 `04-charts/`

| 頁面 | 類型 | 專屬正文應呈現 |
|------|------|----------------|
| [index](04-charts/index.md) | 樞紐 | 圖表分類、依模式選圖、學習順序 |
| [line-charts](04-charts/line-charts.md) | 教學 | 線圖、美國線、趨勢判讀 |
| [intraday-charts](04-charts/intraday-charts.md) | 教學 | 分時圖、盤中時段、當沖/隔日沖用途 |
| [kline-basics](04-charts/kline-basics.md) | 教學 | OHLC、影線、週期選擇 |
| [kline-reading](04-charts/kline-reading.md) | 教學 | 三招讀 K：位置、量能、均線 |
| [candle-patterns](04-charts/candle-patterns.md) | 教學 | 16 種單根型態 + 示意 SVG |
| [candle-quickref](04-charts/candle-quickref.md) | 速查 | 型態一頁表 |
| [candle-combinations](04-charts/candle-combinations.md) | 教學 | 組合型態、晨暮星等 |
| [volume-price](04-charts/volume-price.md) | 教學 | 量價關係、價漲量縮等 |
| [chips-charts](04-charts/chips-charts.md) | 教學 | 籌碼相關圖表類型 |
| [fundamental-charts](04-charts/fundamental-charts.md) | 教學 | 營收柱狀、本益比河流圖等 |
| [market-charts](04-charts/market-charts.md) | 教學 | 大盤、類股排行 |
| [indicator-quickref](04-charts/indicator-quickref.md) | 速查 | 五指標 × 時間框架 |
| [ma](04-charts/ma.md) | 教學 | 均線參數、滯後性、強勢股例外 |
| [macd](04-charts/macd.md) | 教學 | 快慢線、背離、案例連結 |
| [rsi](04-charts/rsi.md) | 教學 | 超買超賣、鈍化 |
| [kd](04-charts/kd.md) | 教學 | 隨機指標、短線用途 |
| [bollinger](04-charts/bollinger.md) | 教學 | 通道、波動放大 |

技術指標頁共通：**滯後性**、**強勢股例外**、**停損**連結、**自我檢查**。

---

### 分析思維 `05-analysis/`

| 頁面 | 專屬正文應呈現 |
|------|----------------|
| [index](05-analysis/index.md) | 六篇地圖、建議閱讀順序 |
| [three-pillars](05-analysis/three-pillars.md) | 基本面／技術／籌碼三面交叉 |
| [fundamental-framework](05-analysis/fundamental-framework.md) | 宏觀→產業→公司拆解 |
| [timeframes](05-analysis/timeframes.md) | 當沖／短／中／長四刻度 |
| [conference](05-analysis/conference.md) | 法說會、重大訊息查證 |
| [cross-market](05-analysis/cross-market.md) | ADR 換算、台指期、夜盤 ATS；**手算折溢價** |
| [active-etf](05-analysis/active-etf.md) | 主動 ETF 持股共識 |

---

### 投資模式 `08-investing/`

| 頁面 | 專屬正文應呈現 |
|------|----------------|
| [index](08-investing/index.md) | 全站知識地圖、模式 × 章節對照 |
| [choose-style](08-investing/choose-style.md) | 五個自問、30 天計畫 |
| [mode-psychology](08-investing/mode-psychology.md) | 各模式心態、心態錯配 |
| [day-trade](08-investing/day-trade.md) | 當沖資格、時段、淨利成本 |
| [overnight](08-investing/overnight.md) | 隔日沖、隔夜風險、T+2 |
| [swing-short](08-investing/swing-short.md) | 短線週期、停損 |
| [swing-mid](08-investing/swing-mid.md) | 中線、週 K、月營收 |
| [long-term](08-investing/long-term.md) | 價值、thesis、長抱 |
| [dividend-investing](08-investing/dividend-investing.md) | **canonical** 存股除權息 |
| [dividend-strategies](08-investing/dividend-strategies.md) | 五種配息策略 |
| [etf-investing](08-investing/etf-investing.md) | ETF 配置、核心衛星 |
| [etf-passive-dca](08-investing/etf-passive-dca.md) | **canonical** 0050 定額、閒錢 |
| [etf-high-dividend](08-investing/etf-high-dividend.md) | 高股息 ETF 誤解 |
| [investment-linked-policy](08-investing/investment-linked-policy.md) | 投資型保單費用差 |
| [insurance-fx-products](08-investing/insurance-fx-products.md) | 外幣帳戶、匯率風險 |

---

### 對號入座 `10-persona/`

見**類型 F**；`index` + 四篇身分分組頁。

---

### 風險與紀律 `06-risk/`

| 頁面 | 專屬正文應呈現 |
|------|----------------|
| [index](06-risk/index.md) | 風控四層、與他章關係 |
| [capital](06-risk/capital.md) | **canonical** 閒錢、認賠殺出、曝險上限 |
| [trading-costs](06-risk/trading-costs.md) | **canonical** 稅費表、損益平衡、期望值手算 |
| [margin-trading](06-risk/margin-trading.md) | 融資融券、維持率、追繳 |
| [stop-loss](06-risk/stop-loss.md) | 停損三層 A/B/C、停利減碼 |
| [discipline](06-risk/discipline.md) | 交易日誌、情緒、當沖不留倉 |
| [emergency-playbook](06-risk/emergency-playbook.md) | 跌停、追繳、除息誤買等情境 |

---

### 老手專區 `09-advanced/`

| 頁面 | 專屬正文應呈現 |
|------|----------------|
| [index](09-advanced/index.md) | 進階路線、先決條件 |
| [research-workflow](09-advanced/research-workflow.md) | thesis、查證、賣出條件 |
| [multi-timeframe](09-advanced/multi-timeframe.md) | 週線日線分 K 三層 |
| [portfolio](09-advanced/portfolio.md) | 配置、再平衡、最大回撤試算 |
| [macro-rotation](09-advanced/macro-rotation.md) | 股債商品輪動框架 |
| [advanced-chips](09-advanced/advanced-chips.md) | 集保大戶、進階籌碼 |
| [event-playbook](09-advanced/event-playbook.md) | 財報、除息、法說事件 |
| [futures-signal](09-advanced/futures-signal.md) | 台指期輔助現股（非炒期貨） |
| [veteran-pitfalls](09-advanced/veteran-pitfalls.md) | 老手常見陷阱清單 |

---

### 實戰案例 `07-cases/`（16 篇 + index）

| 案例 | 主題群 | 應呈現的推理焦點 |
|------|--------|------------------|
| [revenue-turn](07-cases/revenue-turn.md) | 營收 | 月營收 YoY 轉折 |
| [hammer-ma](07-cases/hammer-ma.md) | 技術 | 鎚子線 + 均線 |
| [institutional-flow](07-cases/institutional-flow.md) | 籌碼 | 法人連續買超 |
| [day-trade-risk](07-cases/day-trade-risk.md) | 當沖 | 成本、停損、平倉時間 |
| [valuation-trap](07-cases/valuation-trap.md) | 估值 | 高殖利率陷阱 |
| [macd-divergence](07-cases/macd-divergence.md) | 技術 | 頂背離 |
| [conference-chips](07-cases/conference-chips.md) | 籌碼 | 法說 vs 法人 |
| [gap-breakout](07-cases/gap-breakout.md) | 技術 | 突破缺口 |
| [short-squeeze](07-cases/short-squeeze.md) | 籌碼 | 軋空 |
| [dividend-play](07-cases/dividend-play.md) | 除息 | 填息流程 |
| [etf-dca-drawdown](07-cases/etf-dca-drawdown.md) | ETF | 定額遇大跌 |
| [fund-policy-faq](07-cases/fund-policy-faq.md) | 理財 | 基金保單費用 |
| [macro-rates](07-cases/macro-rates.md) | 總經 | 升息估值取捨 |
| [odd-lot-mistake](07-cases/odd-lot-mistake.md) | 小資 | 零股成本 |
| [ex-dividend-mistake](07-cases/ex-dividend-mistake.md) | 除息 | 搶息、2.11% 健保 |
| [disposal-stock-trap](07-cases/disposal-stock-trap.md) | 限制 | 處置股流動性 |

[index](07-cases/index.md) 為**類型 E** 案例導覽表。

---

### 附錄 `appendix/` 與維護者頁

| 頁面 | 應呈現內容 |
|------|------------|
| [formulas](appendix/formulas.md) | 公式一頁速查 + 手算自檢 |
| [investor-checklist](appendix/investor-checklist.md) | 下單前／除息前／月複盤 10 項勾選 |
| [faq](appendix/faq.md) | 28 題 FAQ（本身即問答，尾段綜合自檢） |
| [taxes-for-costing](appendix/taxes-for-costing.md) | **canonical** 稅費試算；綜所稅邊界 |
| [data-sources](appendix/data-sources.md) | 官方資料源樞紐、TWSE OpenAPI |
| 其餘參考頁 | 見**類型 H** |

---

## 三、章節職責速查（避免寫錯地方）

| 內容 | 應寫在 | 其他頁只許 |
|------|--------|------------|
| 證交稅率、損益平衡、期望值 | `trading-costs.md` | 摘要 + 連結 |
| ETF 三層費用、折溢價 | `etf-costs-and-premium.md` | 摘要 + 連結 |
| 0050 定額、閒錢強調 | `etf-passive-dca.md` | 摘要 + 連結 |
| 存股除權息框架 | `dividend-investing.md` | 摘要 + 連結 |
| 閒錢、認賠殺出 | `capital.md#認賠殺出` | 摘要 + 連結 |
| 領息稅費試算 | `taxes-for-costing.md` | 提及費率 + 連結 |
| 單檔月營收怎麼讀 | `revenue.md`（看表） | 分析頁不重複表格 |

---

## 四、驗收對照

| 檢查項 | 工具／文件 |
|--------|------------|
| 看表 A 模板 | `tests/test_table_coverage.py` |
| 連結與錨點 | `scripts/check_links.py --strict` |
| 圖表資產 | `tests/test_chart_assets.py` |
| 覆蓋等級 | [CONTENT-COVERAGE-MATRIX.md](CONTENT-COVERAGE-MATRIX.md) |
| 投資正確性 | [INVESTMENT-REVIEW-CHECKLIST.md](INVESTMENT-REVIEW-CHECKLIST.md) |

---

## 重點回顧

- 全站只有 **8 種頁面類型**；先認類型再套章節。
- **教學頁**必有學習目標、正文、重點回顧；多數另有**自我檢查**。
- **看表頁**必有手算／導覽練習；**案例頁**必有免責與反思。
- **詞典頁**每詞五表；**樞紐 index** 只導覽不重複教學。
- 數字與費率以 **canonical 章**為準，他頁連結即可。

相關：[寫作規範](STYLE-GUIDE.md) · [架構說明](ARCHITECTURE.md) · [內容覆蓋矩陣](CONTENT-COVERAGE-MATRIX.md)
