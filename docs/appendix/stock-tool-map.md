# 與 Stock Bot 工具對照

## 本篇你會學到

- 教學章節與相鄰 `stock` 專案儀表板功能的對應
- 如何用實作工具練習（選用）

本教學站**可獨立閱讀**。若你已安裝相鄰目錄的 [Stock Bot](https://github.com) 專案（`d:\skymiku\stock`），可用下表對照練習。

啟動儀表板：

```bash
cd ../stock
uv sync
uv run stock-dashboard
```

瀏覽器開啟 `http://localhost:8501`。

## 章節 ↔ 儀表板對照

| 教學章節 | Stock Bot 儀表板區塊 | 說明 |
|----------|----------------------|------|
| [個股總覽表](../03-tables/watchlist.md) | 研究與分析 → 個股總覽 Watchlist | 多檔表格、評分排序 |
| [深入分析分頁](../03-tables/deep-dive-tabs.md) | 個股深入分析 → 全部分頁 | 分析、基本面、技術、籌碼等 |
| [評分量表](../03-tables/scoring.md) | 個股深入分析 → 各因子細項 | 九因子 × 四時間框架 |
| [主動 ETF](../05-analysis/active-etf.md) | 主動 ETF 追蹤、ETF 共識跟單 | 持股快照、共識訊號 |
| [投資模式](../08-investing/index.md) | 依時間框架選策略 | 當沖～ETF 七種模式 |
| [老手專區](../09-advanced/index.md) | 研究流程、評分、深入分析 | 系統化選股與複盤 |
| [月營收表](../03-tables/revenue.md) | 個股深入分析 → 基本面分頁 | 月營收 YoY/MoM |
| [三大法人表](../03-tables/institutional.md) | 個股深入分析 → 籌碼 | 法人買賣超 |
| [融資融券表](../03-tables/margin.md) | 個股深入分析 → 籌碼 | 融資融券餘額 |
| [估值表](../03-tables/valuation.md) | 個股深入分析 → KPI | PER/PBR/殖利率 |
| [財報摘要](../03-tables/financials.md) | 個股深入分析 → 季報 | EPS、三率 |
| [K 線與型態](../04-charts/kline-basics.md) | K 線看板 | 16 種型態自動標記（規則見 [型態速查表](../04-charts/candle-quickref.md)） |
| [技術指標](../04-charts/ma.md) | 個股深入分析 → 技術面 | MA/MACD/RSI/KD |
| [法說會](../05-analysis/conference.md) | LLM 法說分析、台股行事曆 | 法說研究與行事曆 |
| [除權息日程表](../03-tables/dividend-schedule.md) | 個股深入分析 / 公開資訊 | 除權息欄位 |
| [鉅額交易表](../03-tables/block-trade.md) | 個股深入分析 → 籌碼 | 鉅額買賣 |
| [跨市場](../05-analysis/cross-market.md) | 美股/跨市場 | 夜盤連動 |
| [當沖戰情](../07-cases/day-trade-risk.md) | 今日當沖戰情室 | 盤中管線（進階） |
| [術語（開發版）](../02-glossary/index.md) | 策略與文件 → glossary.md | 程式術語對照 |

## 建議練習順序

1. 讀完 [K 線基礎](../04-charts/kline-basics.md) → 開啟 **K 線看板** 對照型態。
2. 讀完 [月營收表](../03-tables/revenue.md) → 在 **個股深入分析** 選一檔看營收曲線。
3. 讀完 [案例一](../07-cases/revenue-turn.md) → 自行找一檔股票重複推理步驟（不分享、不下單亦可）。

## 注意事項

- Stock Bot 含自動交易功能，練習建議先用 `watch` 或 `report` 模式，見該專案 README。
- 工具內評分、LLM 建議屬 **C/B 層參考**，不等於你的 **A 層交易規則**（見 [停損三層](../06-risk/stop-loss.md)）。

## 重點回顧

- 教學站重「理解」；Stock Bot 重「實作與驗證」。
- 對照表幫你少花時間找功能，不取代獨立思考。

返回 [首頁](../index.md) · [資料來源](data-sources.md)
