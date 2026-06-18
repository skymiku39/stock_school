# 內容覆蓋矩陣（維護者）

本頁追蹤 Stock School 各主題的**教學覆蓋等級**，是「全站 A 級」升級的驗收依據。等級定義見 [寫作規範 — 教學覆蓋 A 級標準](STYLE-GUIDE.md#教學覆蓋-a-級標準)。學員可略過本頁。

!!! note "怎麼用這張表"
    新增或潤稿後，更新對應列的等級欄。目標：**詞典內 0 個未處理的 D/E**（邊界詞除外）、**看表 10/10 A**、**主題群案例覆蓋率 100%**。

等級：**A** 完整教學 ｜ **B** 良好（缺案例或在哪看）｜ **C** 基礎（偏速查）｜ **D** 碎片 ｜ **E** 未覆蓋 ｜ **邊界** 刻意只做定義（見 [邊界主題](STYLE-GUIDE.md#邊界主題c-級即達標不追求操作-a)）。

---

## 進度總覽

| 區塊 | 目標 | 現況 |
|------|------|------|
| 詞典條目 | 0 個未處理 D/E（邊界除外） | **達成**（選擇權為邊界） |
| 看表章節（10 篇） | 10 A | **10/10 A** |
| 主題群案例 | 覆蓋率 100% | **達成**（16 篇，群群有案例） |
| 詞典外缺口 | 補入詞典或邊界化 | 國債/升降息/槓桿/對衝/liquidation/ROE/護城河/DCF 已補；選擇權邊界化 |

!!! success "全站 A 級升級已完成主體"
    估值表重寫、總經詞包、看表 10 篇 A 模板、實務閉環頁、案例主題群、模式章自檢均已交付。剩餘 IPO 抽籤、QE/CPI 等屬選配深化，非 A 級驗收阻礙項。

---

## 一、看表章節（03-tables）

所有看表章節已對齊 [看表頁 A 模板](STYLE-GUIDE.md#看表頁-a-模板)，並由 `tests/test_table_coverage.py` 把關。

| 章節 | 等級 | 備註 |
|------|------|------|
| [watchlist.md](03-tables/watchlist.md) | A | 在哪看 + 手算漲跌幅 + 連案例 |
| [deep-dive-tabs.md](03-tables/deep-dive-tabs.md) | A | 全站「在哪看」樞紐 |
| [revenue.md](03-tables/revenue.md) | A | 在哪看 + 手算 MoM + 連案例 |
| [institutional.md](03-tables/institutional.md) | A | 在哪看 + 連案例 |
| [margin.md](03-tables/margin.md) | A | 手算券資比 + 連信用交易 |
| [valuation.md](03-tables/valuation.md) | A | 手算 + 同業比 + 在哪看 + 連案例 |
| [financials.md](03-tables/financials.md) | A | ROE 欄 + 在哪看 + 連案例 |
| [scoring.md](03-tables/scoring.md) | A | 分數低於 50 查證流程 |
| [dividend-schedule.md](03-tables/dividend-schedule.md) | A | 在哪看 + 連案例 |
| [block-trade.md](03-tables/block-trade.md) | A | 在哪看資料源 + 連案例 |

---

## 二、詞典條目（02-glossary）

### 行情與報價

| 條目 | 等級 | canonical |
|------|------|-----------|
| 開盤/最高/最低/收盤/開高低收 | A | [quotes](02-glossary/quotes.md)、[quote-screen](01-basics/quote-screen.md) |
| 昨收/平盤/開高/開低/漲跌幅/成交量 | B | quotes |
| 委買委賣/五檔/內外盤/均價 | B | quote-screen |
| 漲停/跌停/前高/前低 | B | quotes |

### 持倉與交易

| 條目 | 等級 | canonical |
|------|------|-----------|
| 股票/當沖 | A | what-is-stock、position、day-trade |
| 張/持倉/庫存/部位/做多/做空 | B | position |
| 零股 | A | trading-flow#零股（時段/低消/定額）+ 自檢 |
| 限價/市價/IOC/T+2/手續費/證交稅 | B | trading-flow、settlement-fees |

### 損益與停損

| 條目 | 等級 | canonical |
|------|------|-----------|
| 停損/心態錯配 | A | stop-loss、mode-psychology |
| 毛價差/淨利/移動停利/損益兩平/風險報酬比 | B | pnl、trading-costs |
| 認賠殺出 | B | capital#閒錢與生活費 |
| 停利 | A | stop-loss#停利與減碼 + 自檢 |

### 交易行為與心態

| 條目 | 等級 | canonical |
|------|------|-----------|
| 投資論點 thesis | A | research-workflow |
| 開倉/平倉/加減碼/抄底/追高殺低/回檔/反彈/套牢/解套/分批/類股/觀察清單 | B | trading-terms、watchlist |
| 回測（策略） | C | trading-terms |

### 法人與籌碼

| 條目 | 等級 | canonical |
|------|------|-----------|
| 三大法人/融資/融券 | A | chips、institutional、案例 |
| 維持率/追繳/斷頭 | A | margin-trading |
| 外資/投信/自營商/買超賣超/借券/券資比/分點/集保大戶/期現價差/鉅額交易 | B | chips、margin、block-trade |

### 基本面

| 條目 | 等級 | canonical |
|------|------|-----------|
| 月營收/殖利率/毛利率/營益率/淨利率/現金股利/除權息/填息 | A | fundamentals、revenue、dividend、案例 |
| YoY/MoM/QoQ/EPS/PER/PBR/OCF/負債比/股票股利/市值 | B | fundamentals、financials |
| FCF | B | financials（待補獨立五表） |
| ROE | A | [fundamentals#roe](02-glossary/fundamentals.md#roe股東權益報酬率) |
| 護城河 / DCF | A | [fundamentals](02-glossary/fundamentals.md#護城河) |

### 技術面與圖表

| 條目 | 等級 | canonical |
|------|------|-----------|
| K線/量價/均線MA/MACD/RSI/KD/布林 | A | 04-charts、案例 |
| 實體/影線/紅黑K/線圖/分時/日K週K/支撐壓力/超買超賣/黃金死亡交叉/頭肩頂/吞噬/晨暮星 | B | technical、04-charts |

### 市場與進階

| 條目 | 等級 | canonical |
|------|------|-----------|
| 注意股/處置股/全額交割/跳空/軋空/ETF/0050/定期定額/高股息ETF | A | trading-restrictions、market-terms、etf 系列、案例 |
| 多頭空頭/缺口/回補缺口/盤堅盤軟/打底/破底/主力/洗盤/利多出盡/量價背離/共同基金/NAV/被動ETF/006208/內扣費用/折溢價/收益平準金/台指期/大小台/保證金 | B | market-terms、etf-costs、futures-intro |
| 上市/上櫃 | B | market-overview（三層市場比較） |
| 資金行情 | B | market-terms（已互連 macro） |
| 興櫃 | B | market-overview（三層市場比較） |

### 風控

| 條目 | 等級 | canonical |
|------|------|-----------|
| 紀律 | A | discipline、mode-psychology |
| 曝險/資金上限 | B | risk、capital |
| 最大回撤 | C | risk |

### 投資模式

| 條目 | 等級 | canonical |
|------|------|-----------|
| 當沖模式/存股/ETF配置/投資型保單/對號入座/閒錢 | A | 對應專章 |
| 隔日沖/短線/中線/長期/保險成本B | B | 對應專章 |

---

## 三、詞典外缺口（待補入詞典或邊界化）

| 條目 | 等級 | 目標 |
|------|------|------|
| 國債 | A | [macro#國債](02-glossary/macro.md#國債) |
| 升息 / 降息 | A | [macro#升息](02-glossary/macro.md#升息) |
| 槓桿（統一定義） | A | [macro#槓桿](02-glossary/macro.md#槓桿) |
| 對衝 hedge | A | [macro#對衝避險](02-glossary/macro.md#對衝避險) |
| liquidation | A | [macro#強制平倉與清算](02-glossary/macro.md#強制平倉與清算) |
| 護城河 Moat | A | [fundamentals#護城河](02-glossary/fundamentals.md#護城河) |
| DCF 現金流折現 | A | [fundamentals#dcf](02-glossary/fundamentals.md#dcf現金流折現) |
| ROE | A | [fundamentals#roe](02-glossary/fundamentals.md#roe股東權益報酬率) |
| 選擇權 / 期權 | 邊界 | [macro#選擇權](02-glossary/macro.md#選擇權)（定義 + 不教操作） |
| IPO 抽籤 | D | FAQ 級 |
| 綜所稅 / 股利申報 | 邊界 | taxes 邊界說明 |
| QE / CPI / GDP / VIX / ADR | C | abbreviations + 連結 |
| Priced In | B | fundamental-framework（待進詞典） |

---

## 四、主題群案例覆蓋

| 主題群 | 案例 | 狀態 |
|--------|------|------|
| 營收轉折 | [revenue-turn](07-cases/revenue-turn.md) | 有 |
| 技術型態 | [hammer-ma](07-cases/hammer-ma.md)、[macd-divergence](07-cases/macd-divergence.md)、[gap-breakout](07-cases/gap-breakout.md) | 有 |
| 籌碼法人 | [institutional-flow](07-cases/institutional-flow.md)、[conference-chips](07-cases/conference-chips.md) | 有 |
| 估值 | [valuation-trap](07-cases/valuation-trap.md) | 有 |
| 當沖風控 | [day-trade-risk](07-cases/day-trade-risk.md) | 有 |
| 軋空 | [short-squeeze](07-cases/short-squeeze.md) | 有 |
| 除權息 | [dividend-play](07-cases/dividend-play.md) | 有 |
| ETF 定額 | [etf-dca-drawdown](07-cases/etf-dca-drawdown.md) | 有 |
| 基金保單 | [fund-policy-faq](07-cases/fund-policy-faq.md) | 有 |
| 總經利率 | [macro-rates](07-cases/macro-rates.md) | 有 |
| 零股小資 | [odd-lot-mistake](07-cases/odd-lot-mistake.md) | 有 |
| 除息誤操作 | [ex-dividend-mistake](07-cases/ex-dividend-mistake.md) | 有 |
| 處置股 | [disposal-stock-trap](07-cases/disposal-stock-trap.md) | 有 |

---

## 重點回顧

- 本表是 A 級升級的**唯一進度依據**，等級定義以 [寫作規範](STYLE-GUIDE.md#教學覆蓋-a-級標準) 為準。
- 邊界主題維持 C／邊界即達標，不視為缺口。
- 每波交付後務必同步更新本表。
