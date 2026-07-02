# 內容覆蓋矩陣（維護者）

本頁追蹤 Stock School 各主題的**教學覆蓋等級**，是「全站 A 級」升級的驗收依據。等級定義見 [寫作規範 — 教學覆蓋 A 級標準](STYLE-GUIDE.md#教學覆蓋-a-級標準)。學員可略過本頁。

!!! note "怎麼用這張表"
    新增或潤稿後，更新對應列的等級欄。目標：**詞典內 0 個未處理的 D/E**（邊界詞除外）、**看表 10/10 A**、**主題群案例覆蓋率 100%**。全站逐篇複審進度見 [逐篇複審計畫](ARTICLE-REVIEW-PLAN.md)。

等級：**A** 完整教學 ｜ **B** 良好（缺案例或在哪看）｜ **C** 基礎（偏速查）｜ **D** 碎片 ｜ **E** 未覆蓋 ｜ **邊界** 刻意只做定義（見 [邊界主題](STYLE-GUIDE.md#邊界主題c-級即達標不追求操作-a)）。

---

## 進度總覽

| 區塊 | 目標 | 現況 |
|------|------|------|
| 詞典條目 | 0 個未處理 D/E（邊界除外） | **達成**（選擇權為邊界） |
| 看表章節（10 篇） | 10 嚴格 A | **10/10 嚴格 A**（含手算／導覽練習，`test_table_coverage.py` 把關） |
| 主題群案例 | 覆蓋率 100% | **達成**（16 篇，群群有案例） |
| 詞典外缺口 | 補入詞典或邊界化 | 國債/升降息/槓桿/對衝/liquidation/ROE/護城河/DCF/CPI/GDP/IPO/ADR 已補；選擇權邊界化 |
| 外部官方資料源 | 關鍵主題接官方來源 | **已補**：TDCC、央行、FRED、DGBAS、MOPS 重訊、TWSE OpenAPI、第三方平台映射 |
| P2 canonical 自檢 | 14 頁章末自檢 | **已補**（見下方 P2 清單） |
| P3 技術面 canonical | 8 頁圖表自檢 | **已補**（見下方 P3 清單） |
| P3 延伸 04-charts | 7 頁專題圖表自檢 | **已補**（見下方 P3 延伸清單） |
| P4 詞典缺口 | FCF、最大回撤、Priced In、QE/VIX | **已補**（見下方 P4 清單） |
| 稅務邊界 | 綜所稅／申報邊界說明 | **已補**（[taxes-for-costing](appendix/taxes-for-costing.md#綜所稅與申報邊界)） |
| Phase 6 投資模式 | 各模式專章章末自檢 | **已補**（14/14 非 index 頁，見下方清單） |
| 05-analysis 教學頁 | 6 篇 canonical 自檢 | **已補**（見下方 05-analysis 清單） |
| 09-advanced portfolio | 組合管理自檢 | **已補**（[portfolio#自我檢查](09-advanced/portfolio.md)） |
| 09-advanced 其餘 5 篇 | 老手專區章末自檢 | **已補**（見下方 09-advanced 清單） |
| 06-risk 風控專章 | 6 篇章末自檢 | **已補**（見下方 06-risk 清單） |
| 01-basics 入門 | 16 篇章末自檢 | **已補**（見下方 01-basics 清單） |
| 10-persona 分頁 | 4 篇身分分組自檢 | **已補**（見下方 10-persona 清單） |
| 附錄教學頁 | 公式／清單／資料源／FAQ 自檢 | **已補**（`taxes-for-costing` 先前已補） |
| 02-glossary 分類頁 | 8 篇詞典分類自檢 | **已補**（`macro`／`fundamentals` 先前已補） |
| 專章樞紐 index | 8 篇導覽頁自檢 | **已補**（見下方樞紐清單） |

!!! success "看表嚴格 A 已達標"
    看表 10 篇均已含手算一例（或樞紐頁導覽練習一例）與完整 A 模板；`tests/test_table_coverage.py` 同步檢查手算／導覽練習區塊。

!!! success "P0～P4 主軸與 Phase 6 模式章已交付"
    看表 10/10 嚴格 A、主題群案例 100%、canonical 教學頁與 04-charts 延伸自檢、稅務邊界、投資模式 14 章自檢均已補齊；詞典大量 B 為刻意設計（五表 + canonical 連結），邊界詞維持 C／邊界。

!!! note "全站其餘主題"
    `04-charts` 速查頁（`indicator-quickref`、`candle-quickref`）維持 **C 級速查定位**，已補精簡章末自檢並連結完整教學頁；邊界主題（綜所稅申報）已於 [稅務試算](appendix/taxes-for-costing.md#綜所稅與申報邊界) 標示邊界與站外查詢。

---

## 一、看表章節（03-tables）

所有看表章節已對齊 [看表頁 A 模板](STYLE-GUIDE.md#看表頁-a-模板)，並由 `tests/test_table_coverage.py` 把關（含 `## 手算一例` 或 `## 導覽練習一例`）。

| 章節 | 等級 | 備註 |
|------|------|------|
| [watchlist.md](03-tables/watchlist.md) | A | 手算漲跌幅 + 連案例 |
| [deep-dive-tabs.md](03-tables/deep-dive-tabs.md) | A | 樞紐頁；**導覽練習一例**（豁免單欄手算） |
| [revenue.md](03-tables/revenue.md) | A | 手算 MoM + 連案例 |
| [institutional.md](03-tables/institutional.md) | A | 手算法人合計 + 連案例 |
| [margin.md](03-tables/margin.md) | A | 手算券資比 + 連信用交易 |
| [valuation.md](03-tables/valuation.md) | A | 手算 PER/PBR/殖利率 + 連案例 |
| [financials.md](03-tables/financials.md) | A | 手算淨利率 + `## 常見誤區` + 連案例 |
| [scoring.md](03-tables/scoring.md) | A | 手算框架分差 + 低於 50 查證流程 |
| [dividend-schedule.md](03-tables/dividend-schedule.md) | A | 手算殖利率反推 + 連案例 |
| [block-trade.md](03-tables/block-trade.md) | A | 手算鉅額金額 + 連案例 |

### P2 canonical 頁（已補章末自檢）

| 頁面 | 補強 |
|------|------|
| [what-is-stock](01-basics/what-is-stock.md) | 常見誤區 + 自檢 |
| [research-workflow](09-advanced/research-workflow.md) | 常見誤區 + 自檢 |
| [discipline](06-risk/discipline.md) | 自檢 |
| [capital](06-risk/capital.md) | 自檢 |
| [mode-psychology](08-investing/mode-psychology.md) | 自檢 |
| [etf-passive-dca](08-investing/etf-passive-dca.md) | 自檢 |
| [10-persona/index](10-persona/index.md) | 自檢 |
| [cross-market](05-analysis/cross-market.md) | 常見誤區 + 自檢 |
| [conference](05-analysis/conference.md) | 常見誤區 + 自檢 |
| [advanced-chips](09-advanced/advanced-chips.md) | 自檢 |
| [etf-intro](01-basics/etf-intro.md) | 常見誤區 + 自檢 |
| [trading-restrictions](01-basics/trading-restrictions.md) | 自檢 |
| [macro](02-glossary/macro.md) | 頁末自檢 |
| [fundamentals](02-glossary/fundamentals.md) | 頁末自檢 |

### P3 技術面 canonical（已補章末自檢）

| 頁面 | 補強 |
|------|------|
| [kline-basics](04-charts/kline-basics.md) | 常見誤區 + 自檢 |
| [kline-reading](04-charts/kline-reading.md) | 常見誤區 + 自檢 |
| [ma](04-charts/ma.md) | 自檢 |
| [macd](04-charts/macd.md) | 自檢 |
| [rsi](04-charts/rsi.md) | 自檢 |
| [kd](04-charts/kd.md) | 自檢 |
| [bollinger](04-charts/bollinger.md) | 自檢 |
| [volume-price](04-charts/volume-price.md) | 常見誤區 + 自檢 |

### P3 延伸 04-charts（已補章末自檢）

| 頁面 | 補強 |
|------|------|
| [candle-patterns](04-charts/candle-patterns.md) | 常見誤區 + 自檢 |
| [candle-combinations](04-charts/candle-combinations.md) | 常見誤區 + 自檢 |
| [intraday-charts](04-charts/intraday-charts.md) | 常見誤區 + 自檢 |
| [line-charts](04-charts/line-charts.md) | 自檢 |
| [fundamental-charts](04-charts/fundamental-charts.md) | 常見誤區 + 自檢 |
| [chips-charts](04-charts/chips-charts.md) | 常見誤區 + 自檢 |
| [market-charts](04-charts/market-charts.md) | 常見誤區 + 自檢 |

### 04-charts 速查頁（C 級 + 精簡自檢）

| 頁面 | 補強 |
|------|------|
| [indicator-quickref](04-charts/indicator-quickref.md) | 精簡自檢（連結完整指標教學） |
| [candle-quickref](04-charts/candle-quickref.md) | 精簡自檢（連結 candle-patterns） |

### Phase 6 投資模式（已補章末自檢）

| 頁面 | 補強 |
|------|------|
| [day-trade](08-investing/day-trade.md) | 自檢 |
| [overnight](08-investing/overnight.md) | 自檢 |
| [swing-short](08-investing/swing-short.md) | 自檢 |
| [swing-mid](08-investing/swing-mid.md) | 自檢 |
| [long-term](08-investing/long-term.md) | 自檢 |
| [dividend-investing](08-investing/dividend-investing.md) | 自檢 |
| [dividend-strategies](08-investing/dividend-strategies.md) | 自檢 |
| [etf-investing](08-investing/etf-investing.md) | 自檢 |
| [etf-passive-dca](08-investing/etf-passive-dca.md) | 自檢 |
| [etf-high-dividend](08-investing/etf-high-dividend.md) | 自檢 |
| [choose-style](08-investing/choose-style.md) | 自檢 |
| [mode-psychology](08-investing/mode-psychology.md) | 自檢 |
| [insurance-fx-products](08-investing/insurance-fx-products.md) | 自檢 |
| [investment-linked-policy](08-investing/investment-linked-policy.md) | 自檢 |

### 05-analysis 教學頁（已補章末自檢）

| 頁面 | 補強 |
|------|------|
| [three-pillars](05-analysis/three-pillars.md) | 自檢 |
| [fundamental-framework](05-analysis/fundamental-framework.md) | 自檢 |
| [timeframes](05-analysis/timeframes.md) | 自檢 |
| [cross-market](05-analysis/cross-market.md) | 常見誤區 + 自檢 |
| [conference](05-analysis/conference.md) | 常見誤區 + 自檢 |
| [active-etf](05-analysis/active-etf.md) | 自檢 |

### 09-advanced 老手專區（已補章末自檢）

| 頁面 | 補強 |
|------|------|
| [research-workflow](09-advanced/research-workflow.md) | 常見誤區 + 自檢 |
| [advanced-chips](09-advanced/advanced-chips.md) | 自檢 |
| [portfolio](09-advanced/portfolio.md) | 自檢 |
| [veteran-pitfalls](09-advanced/veteran-pitfalls.md) | 自檢 |
| [macro-rotation](09-advanced/macro-rotation.md) | 自檢 |
| [multi-timeframe](09-advanced/multi-timeframe.md) | 自檢 |
| [event-playbook](09-advanced/event-playbook.md) | 自檢 |
| [futures-signal](09-advanced/futures-signal.md) | 自檢 |

### 06-risk 風控專章（已補章末自檢）

| 頁面 | 補強 |
|------|------|
| [trading-costs](06-risk/trading-costs.md) | 自檢 |
| [margin-trading](06-risk/margin-trading.md) | 常見誤區 + 自檢 |
| [emergency-playbook](06-risk/emergency-playbook.md) | 自檢 |
| [stop-loss](06-risk/stop-loss.md) | 自檢 |
| [discipline](06-risk/discipline.md) | 自檢 |
| [capital](06-risk/capital.md) | 自檢 |

### 01-basics 入門專章（已補章末自檢）

| 頁面 | 補強 |
|------|------|
| [what-is-stock](01-basics/what-is-stock.md) | 常見誤區 + 自檢 |
| [open-account](01-basics/open-account.md) | 自檢 |
| [first-trade-walkthrough](01-basics/first-trade-walkthrough.md) | 自檢 |
| [trading-flow](01-basics/trading-flow.md) | 自檢 |
| [settlement-fees](01-basics/settlement-fees.md) | 自檢 |
| [quote-screen](01-basics/quote-screen.md) | 自檢 |
| [price-and-cap](01-basics/price-and-cap.md) | 自檢 |
| [roles](01-basics/roles.md) | 自檢 |
| [market-overview](01-basics/market-overview.md) | 自檢 |
| [trading-restrictions](01-basics/trading-restrictions.md) | 自檢 |
| [dividend](01-basics/dividend.md) | 自檢 |
| [etf-intro](01-basics/etf-intro.md) | 常見誤區 + 自檢 |
| [etf-costs-and-premium](01-basics/etf-costs-and-premium.md) | 自檢 |
| [mutual-fund-intro](01-basics/mutual-fund-intro.md) | 自檢 |
| [futures-intro](01-basics/futures-intro.md) | 自檢 |
| [ipo-subscription](01-basics/ipo-subscription.md) | 自檢 |

### 10-persona 身分分組（已補章末自檢）

| 頁面 | 補強 |
|------|------|
| [index](10-persona/index.md) | 自檢（P2 canonical） |
| [beginner](10-persona/beginner.md) | 自檢 |
| [steady](10-persona/steady.md) | 自檢 |
| [busy](10-persona/busy.md) | 自檢 |
| [active](10-persona/active.md) | 自檢 |

### 附錄教學頁（已補章末自檢）

| 頁面 | 補強 |
|------|------|
| [formulas](appendix/formulas.md) | 手算 + 自檢 |
| [investor-checklist](appendix/investor-checklist.md) | 自檢 |
| [data-sources](appendix/data-sources.md) | 自檢 |
| [faq](appendix/faq.md) | 綜合自檢 |
| [taxes-for-costing](appendix/taxes-for-costing.md) | 自檢 + 綜所稅邊界 |

### 02-glossary 分類頁（已補章末自檢）

| 頁面 | 補強 |
|------|------|
| [fundamentals](02-glossary/fundamentals.md) | 頁末自檢（P2 canonical） |
| [macro](02-glossary/macro.md) | 頁末自檢（P2 canonical） |
| [chips](02-glossary/chips.md) | 自檢 |
| [trading-terms](02-glossary/trading-terms.md) | 自檢 |
| [technical](02-glossary/technical.md) | 自檢 |
| [risk](02-glossary/risk.md) | 自檢 |
| [position](02-glossary/position.md) | 自檢 |
| [quotes](02-glossary/quotes.md) | 自檢 |
| [pnl](02-glossary/pnl.md) | 自檢 |
| [market-terms](02-glossary/market-terms.md) | 自檢 |

### 專章樞紐 index（已補章末自檢）

| 頁面 | 補強 |
|------|------|
| [03-tables/index](03-tables/index.md) | 自檢 |
| [04-charts/index](04-charts/index.md) | 自檢 |
| [05-analysis/index](05-analysis/index.md) | 自檢 |
| [06-risk/index](06-risk/index.md) | 自檢 |
| [07-cases/index](07-cases/index.md) | 自檢 |
| [08-investing/index](08-investing/index.md) | 自檢 |
| [09-advanced/index](09-advanced/index.md) | 自檢 |
| [02-glossary/index](02-glossary/index.md) | 自檢 |

### P4 詞典／進階缺口（已補）

| 主題 | 頁面 |
|------|------|
| FCF 五表 | [fundamentals#fcf](02-glossary/fundamentals.md#fcf自由現金流) |
| 最大回撤試算 | [portfolio#最大回撤試算](09-advanced/portfolio.md#最大回撤試算) |
| Priced In | [market-terms#priced-in](02-glossary/market-terms.md#priced-in) |
| QE / VIX | [macro#量化寬鬆](02-glossary/macro.md#量化寬鬆qe)、[#vix](02-glossary/macro.md#vix) |

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
| 認賠殺出 | B | capital#認賠殺出 |
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
| 外資/投信/自營商/買超賣超/借券/券資比/分點/期現價差/鉅額交易 | B | chips、margin、block-trade |
| 集保大戶/股權分散表 | A | advanced-chips#集保大戶（TDCC、ID 歸戶、設質專戶） |

### 基本面

| 條目 | 等級 | canonical |
|------|------|-----------|
| 月營收/殖利率/毛利率/營益率/淨利率/現金股利/除權息/填息 | A | fundamentals、revenue、dividend、案例 |
| YoY/MoM/QoQ/EPS/PER/PBR/OCF/負債比/股票股利/市值 | B | fundamentals、financials |
| FCF | A | [fundamentals#fcf](02-glossary/fundamentals.md#fcf自由現金流) |
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
| 上市/上櫃 | A | [quotes#上市](02-glossary/quotes.md#上市)、[quotes#上櫃](02-glossary/quotes.md#上櫃)、[market-overview](01-basics/market-overview.md) |
| 資金行情 | B | market-terms（已互連 macro） |
| 興櫃 | B | market-overview（三層市場比較） |

### 風控

| 條目 | 等級 | canonical |
|------|------|-----------|
| 紀律 | A | discipline、mode-psychology |
| 曝險/資金上限 | B | risk、capital |
| 最大回撤 | A | [risk](02-glossary/risk.md) + [portfolio#最大回撤試算](09-advanced/portfolio.md#最大回撤試算) |

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
| IPO 抽籤 | A | [ipo-subscription](01-basics/ipo-subscription.md)（機制+退款+資金虹吸+自檢） |
| 綜所稅 / 股利申報 | 邊界 | [taxes-for-costing#綜所稅與申報邊界](appendix/taxes-for-costing.md#綜所稅與申報邊界)（邊界 + 站外查詢 + 自檢） |
| CPI / GDP | A | [macro#cpi](02-glossary/macro.md#cpi)、[#gdp](02-glossary/macro.md#gdp)（DGBAS 來源） |
| ADR / 夜盤 | A | [cross-market](05-analysis/cross-market.md#adr-折溢價怎麼算)（換算/折溢價/ATS） |
| 殖利率曲線倒掛 | A | [macro#殖利率曲線倒掛](02-glossary/macro.md#殖利率曲線倒掛)（FRED T10Y2Y） |
| QE / VIX | A | [macro#量化寬鬆](02-glossary/macro.md#量化寬鬆qe)、[#vix](02-glossary/macro.md#vix) |
| Priced In | A | [market-terms#priced-in](02-glossary/market-terms.md#priced-in) |

### 外部官方資料源整合對照

| 外部源 | 接入章節 |
|--------|----------|
| 集保 TDCC 股權分散表 | [advanced-chips#集保大戶](09-advanced/advanced-chips.md#集保大戶)、[chips](02-glossary/chips.md) |
| 央行三大政策利率 | [macro#升息](02-glossary/macro.md#升息) |
| FRED 美債（DGS10/T10Y2Y/T10Y3M/DFII10） | [macro#國債](02-glossary/macro.md#國債)、[data-sources](appendix/data-sources.md#fred-常用代碼) |
| 主計總處 DGBAS（CPI/GDP） | [macro#cpi](02-glossary/macro.md#cpi) |
| MOPS 重大訊息 | [conference](05-analysis/conference.md) |
| 官方估值防呆 / OpenAPI 估值端點 | [valuation#官方計算與防呆](03-tables/valuation.md#官方計算與防呆) |
| ADR 換算 / 美股夜盤 ATS | [cross-market](05-analysis/cross-market.md) |
| IPO 申購（證交所/櫃買承銷） | [ipo-subscription](01-basics/ipo-subscription.md) |
| TWSE OpenAPI / 第三方平台映射 | [data-sources](appendix/data-sources.md#twse-openapi自動化串接) |

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
