# 進階：學員詞與 Stock Bot 對照

## 本篇你會學到

- 教學站中文術語與相鄰 Stock Bot 程式/欄位的對應
- 何時需要查這張表

本站 [術語詞典](../02-glossary/index.md) 以**學員語言**為主，不出現程式名。若你使用 [Stock Bot 工具對照](stock-tool-map.md) 或閱讀 `stock` 專案文件，可用本表對照。

## 代號與行情

| 學員說法 | Stock Bot / 程式 | 說明 |
|----------|------------------|------|
| 代號、股票代碼 | `symbol`（交易）/ `ticker`（評分、LLM） | 兩者同義 |
| 漲跌幅 | `pct_chg` / `pct_change` | 同一概念不同模組命名 |

## 損益與停損三層

| 學員說法 | 程式 / 設定 | 說明 |
|----------|-------------|------|
| 淨利 % | `net_pnl_pct()`、`position_net_pnl_pct()` | 扣費損後 |
| A 層實際停損 | `STOP_LOSS_PCT`（`.env`） | 見 [停損三層](../06-risk/stop-loss.md) |
| A 層移動停利 | `TAKE_PROFIT_PCT`、`TRAILING_STOP_PCT` | 啟動門檻 + 回撤 |
| C 層評分建議 | `scoring.py` → `STRATEGY_RULES` | 當沖 -1%/+2% 等 |
| B 層戰情建議 | `intraday_brief` 等 prompt 輸出 | 人工參考 |

## 持倉

| 學員說法 | 程式 | 說明 |
|----------|------|------|
| 持倉 | `PositionInfo`、`positions` | 策略追蹤 |
| 庫存 | `broker.list_positions()` | 券商實際持股 |
| AI 標記部位 | `owner_tag=AI` | 允許自動賣出的條件之一 |

## 風控

| 學員說法 | 程式 | 說明 |
|----------|------|------|
| 交易可行性檢查 | `run_preflight()` | 7 分區 |
| 12 道閘門 | `RiskGuard.check_entry()` | 每筆買單前 |
| 緊急停機 | `data/.kill_switch` | 擋新進場 |

## 評分九因子

| 學員說法 | scoring 因子 key | 說明 |
|----------|------------------|------|
| 技術面 | `technical` | MA/MACD/RSI 等 |
| 籌碼面 | `chips` | 法人、融資 |
| 基本面 | `fundamental` | 營收、估值 |
| 法說情緒 | `llm_sentiment` | LLM 解析 |
| 言行邏輯 | `logic` | 法說 vs 籌碼 |
| ETF 共識 | `etf_consensus` | 主動 ETF |
| 大戶結構 | `distribution` | 集保 |
| 美股連動 | `us_market` | 跨市場 |
| 風險警示 | `risk` | 異常籌碼 |

詳見 [評分量表](../03-tables/scoring.md)。

## K 線型態

| 學員說法 | 程式 | 說明 |
|----------|------|------|
| 16 種 K 棒型態 | `candle_patterns.classify_candle()` | 規則見 [16 種型態](../04-charts/candle-patterns.md) |

## 執行模式

| 學員說法 | `RUN_MODE` | 說明 |
|----------|------------|------|
| 自動下單 | `trade` | 實單/模擬 |
| 看盤不下單 | `watch` | 虛擬訊號 |
| 純報表 | `report` | 延遲資料 |

## 重點回顧

- 學員詞典用於學習；本表用於對接 Stock Bot。
- 程式命名以 `stock/docs/glossary.md` 為開發者權威來源。

相關：[工具對照](stock-tool-map.md) · [資料來源](data-sources.md)
