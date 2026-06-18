# 資料來源說明

## 本篇你會學到

- 台股與總經常見公開資料從哪裡來、官方網址
- 各資料源的更新頻率與限制
- 如何把官方來源接到本站各章

!!! tip "這頁是全站外部資料樞紐"
    各教學頁的「在哪裡看到」最終都指向本頁。想實際查真實數據（而非站內教學示意），從這裡找官方入口。

## 官方與交易所

| 來源 | 網址 | 常見資料 |
|------|------|----------|
| **公開資訊觀測站（MOPS）** | [mops.twse.com.tw](https://mops.twse.com.tw) | 財報、月營收、重大訊息、法說會 |
| **MOPS 重大訊息查詢** | [t05sr01_1](https://mops.twse.com.tw/mops/web/t05sr01_1) | 即時重大訊息（事件驅動查證） |
| **台灣證券交易所** | [twse.com.tw](https://www.twse.com.tw) | 上市行情、三大法人、融資融券 |
| **櫃買中心（TPEx）** | [tpex.org.tw](https://www.tpex.org.tw) | 上櫃行情與法人、櫃買指數（OTC） |
| **集保結算所（TDCC）** | [tdcc.com.tw 股權分散表](https://www.tdcc.com.tw/portal/zh/smWeb/qryStock) | 集保戶股權分散表（大戶／散戶結構） |
| **臺灣期貨交易所** | [taifex.com.tw](https://www.taifex.com.tw) | 期貨／選擇權保證金、契約規格、稅率 |

## 總體經濟與利率 {#總體經濟與利率}

| 來源 | 網址 | 常見資料 |
|------|------|----------|
| **中央銀行（CBC）** | [cbc.gov.tw](https://www.cbc.gov.tw) | 重貼現率等三大政策利率、貨幣政策 |
| **主計總處（DGBAS）** | [dgbas.gov.tw](https://www.dgbas.gov.tw) | GDP 經濟成長率、CPI 消費者物價（含核心 CPI）|
| **美國 FRED** | [fred.stlouisfed.org](https://fred.stlouisfed.org) | 美國公債殖利率等全球利率時間序列 |

### FRED 常用代碼 {#fred-常用代碼}

| 代碼 | 指標 | 用途 |
|------|------|------|
| [DGS10](https://fred.stlouisfed.org/series/DGS10) | 10 年期公債殖利率（日） | 全球無風險利率、[DCF](../02-glossary/fundamentals.md#dcf現金流折現) 折現率參考 |
| GS10 | 10 年期公債殖利率（月） | 同上，月頻率 |
| T10Y2Y | 10 年減 2 年利差 | 殖利率曲線，負值（倒掛）常預示衰退 |
| T10Y3M | 10 年減 3 月利差 | 紐約聯準銀行衰退機率模型基準 |
| DFII10 | 10 年期抗通膨債殖利率 | 實質利率代理；名目−實質≈預期通膨 |

詳見 [總經與利率術語](../02-glossary/macro.md)。

## 行情與歷史資料

| 來源 | 說明 |
|------|------|
| TWSE OpenAPI | 日 K、估值、漲跌幅限制、ESG（程式常用，見下節） |
| 券商看盤軟體 | 即時報價、五檔（需開戶） |

## 籌碼與持股

| 資料 | 更新 | 注意 |
|------|------|------|
| 三大法人買賣超 | T+1 | 非即時 |
| 融資融券餘額 | T+1 | 口徑依交易所 |
| 集保股權分散表（TDCC） | 每週（週六上午後） | 以週五登摺餘額為準，ID 跨券商歸戶 |

集保表的歸戶、設質專戶、融券／借券對籌碼的影響，見 [進階籌碼解讀](../09-advanced/advanced-chips.md#集保大戶)。

## 基本面與估值

| 資料 | 來源 |
|------|------|
| 月營收 | MOPS，次月 10 日前 |
| 季報 | MOPS，季後法定時限 |
| 除權息 | 交易所公告 |
| 每日 PER／PBR／殖利率 | TWSE OpenAPI `/exchangeReport/STOCK_DAY_AVG_ALL` |

## 初級市場（IPO 公開申購） {#初級市場ipo-公開申購}

| 資料 | 來源 |
|------|------|
| 申購公告、承銷價、抽籤日、撥券日 | 證交所 / 櫃買中心承銷公告 |

詳見 [IPO 公開申購（抽籤）](../01-basics/ipo-subscription.md)。

## 跨市場（參考用） {#跨市場參考用}

| 來源 | 資料 |
|------|------|
| yfinance 等 | 美股、指數、部分 ADR |
| 美股夜盤（ATS，如 Blue Ocean） | 亞洲時段美股報價，台股開盤前領先指標 |

ADR 換算與夜盤機制見 [跨市場連動](../05-analysis/cross-market.md)。

## 第三方財經平台（官方資料的轉譯）

官方介面以合規與羅列為主，缺視覺化；實務常用第三方平台輔助，但須對照官方底層定義。

| 平台 | 常見呈現 | 對應官方底層 |
|------|----------|--------------|
| Yahoo 股市 / Goodinfo / CMoney | PER／PBR／殖利率欄、財報趨勢圖 | TWSE/TPEx 估值、MOPS 財報 |
| 各站「本益比 N/A」 | 顯示為空值 | 依證交所規範：近四季 EPS 加總為負 → 防呆不計算（非資料缺失），見 [估值表](../03-tables/valuation.md#官方計算與防呆) |

!!! warning "口徑一致"
    第三方數字可能用不同 EPS 基準或匯率，**比較時固定同一來源**，並以官方公告為最終依據。

## TWSE OpenAPI（自動化串接） {#twse-openapi自動化串接}

| 項目 | 內容 |
|------|------|
| Base URL | `https://openapi.twse.com.tw/v1` |
| 規格文件 | [swagger.json](https://openapi.twse.com.tw/v1/swagger.json)（OAS 2.0）|
| 授權 | 多數採政府資料開放平台規範，免費、免憑證 |

常用端點：

| 端點 | 資料 |
|------|------|
| `/exchangeReport/STOCK_DAY_AVG_ALL` | 上市個股日 PER／殖利率／PBR |
| `/exchangeReport/STOCK_DAY_ALL` | 盤後開高低收、成交量 |
| `TWT84U`（漲跌幅限制） | 每日漲跌停價、開盤競價基準（風控邊界） |
| `/opendata/t187ap46_L_1` 等 | ESG：溫室氣體、燃料、資安等非財務指標 |

!!! note "資料新鮮度（維護者）"
    盤後資訊約於交易日 **13:50** 後才產製。自動化排程（Python／GAS）建議設在 **14:00 後**，避免抓到空值或前一日舊資料；歷史補齊請改用證交所歷史查詢頁。本站產圖流程見 [架構說明](../ARCHITECTURE.md)。

## 各看表去哪查

對照 [怎麼看表總覽](../03-tables/index.md)，每張表的資料來源：

| 看表章節 | 主要來源 | 更新 |
|----------|----------|------|
| [個股總覽表](../03-tables/watchlist.md) | 券商行情、排行榜 | 即時／盤後 |
| [月營收表](../03-tables/revenue.md) | MOPS 月營收 | 次月 10 日前 |
| [三大法人表](../03-tables/institutional.md) | 證交所／櫃買 | T+1 |
| [融資融券表](../03-tables/margin.md) | 證交所／櫃買 | T+1 |
| [估值表](../03-tables/valuation.md) | MOPS、財經網站 | 隨財報／每日股價 |
| [財報摘要表](../03-tables/financials.md) | MOPS 財務報表 | 季報法定時限 |
| [除權息日程表](../03-tables/dividend-schedule.md) | MOPS、交易所公告 | 公告制 |
| [鉅額交易表](../03-tables/block-trade.md) | 證交所／櫃買鉅額日報 | 盤後／次日 |

## 使用原則

1. **以官方公告為準**：媒體標題僅作線索。
2. **注意 lag**：籌碼 T+1、集保週更，不適合當唯一即時依據。
3. **口徑一致**：不同網站 PER、法人合計可能略有差異，比較時用同一來源。

## 重點回顧

- MOPS + 交易所 + TDCC + 央行/FRED 是台股與總經的權威來源。
- 第三方平台方便，但要對照官方底層定義（如本益比 N/A 的防呆）。
- 即時交易需券商行情；本教學站不要求即時資料。

相關：[工具對照](stock-tool-map.md) · [總經與利率](../02-glossary/macro.md) · [跨市場連動](../05-analysis/cross-market.md) · [IPO 公開申購](../01-basics/ipo-subscription.md)
