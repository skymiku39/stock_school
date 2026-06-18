# 圖表檢查清單（維護者）

本頁是 Stock School 圖表資產的**驗收依據**，供維護者在新增圖表、改動產圖程式或發布前逐項檢查。學員可略過本頁。

!!! note "定位"
    本頁規範「如何檢查圖表完整性」；圖表如何產生請見 [架構說明](ARCHITECTURE.md)，寫作規範請見 [寫作規範](STYLE-GUIDE.md)。

---

## 圖表資產總覽

| 類型 | 數量 | 產生方式 | 是否需要網路 |
|------|------|----------|--------------|
| 教學 SVG | 52 張（另含 `logo.svg`） | `scripts/stock_school/render/` → `docs/assets/` | 部分需要 |
| Mermaid 圖 | 93 個 / 73 檔 | Markdown fenced block + `mkdocs-mermaid2-plugin` | 否 |

教學 SVG 依產生器分為五類，**只有報價與技術指標需要 TWSE 連線**；其餘為合成教學數據，離線即可重現。

---

## 預期 SVG 清單

### 報價類 `docs/assets/quotes/`（需網路 · 8 張）

每檔股票 4 張：`{code}-quote-screen.svg`、`{code}-daily-k.svg`、`{code}-intraday-demo.svg`、`{code}-volume.svg`，code 為 `2330` 與 `0050`。

### K 線型態 `docs/assets/candles/`（離線 · 21 張）

`structure.svg` + 16 種單根型態（大/中/小紅黑 K、倒鎚紅黑、紅黑鎚子、紡錘紅黑、十字、T 字、倒 T、一字）+ 4 種組合（看漲/看跌吞噬、晨星、暮星）。

### 技術指標 `docs/assets/indicators/`（需網路 · 9 張）

`2330-ma.svg`、`2330-macd.svg`、`2330-rsi.svg`、`2330-kd.svg`、`2330-bollinger.svg`、`2330-volume-price.svg`、`line-compare.svg`、`revenue-demo.svg`、`0050-market.svg`。

### 案例圖 `docs/assets/cases/`（離線 · 8 張）

`hammer-ma.svg`、`macd-divergence.svg`、`gap-breakout.svg`、`etf-dca-drawdown.svg`、`etf-vs-stock.svg`、`valuation-trap.svg`、`conference-chips.svg`、`institutional-flow.svg`。

### 概念示意 `docs/assets/concepts/`（離線 · 6 張）

`institutional-cumulative.svg`、`margin-balance.svg`（籌碼）、`eps-trend.svg`、`profit-margins.svg`、`valuation-band.svg`（基本面）、`sector-performance.svg`（大盤類股）。

---

## 八大圖表分類覆蓋

依 [圖表總覽](04-charts/index.md) 的八大分類，每類至少有一張 SVG 示意：

| 分類 | 代表 SVG |
|------|----------|
| K 線/蠟燭 | `candles/` 全系列 |
| 線圖/美國線 | `indicators/line-compare.svg` |
| 分時圖 | `quotes/{code}-intraday-demo.svg` |
| 量價圖 | `indicators/2330-volume-price.svg`、`quotes/{code}-volume.svg` |
| 籌碼圖 | `concepts/institutional-cumulative.svg`、`concepts/margin-balance.svg` |
| 基本面圖 | `indicators/revenue-demo.svg`、`concepts/eps-trend.svg`、`concepts/profit-margins.svg`、`concepts/valuation-band.svg` |
| 技術指標 | `indicators/2330-*.svg` |
| 大盤圖 | `indicators/0050-market.svg`、`concepts/sector-performance.svg` |

---

## 分層檢查清單

### Phase A — 資產存在性（每次產圖後）

- [ ] `uv run python scripts/generate_all.py` 無例外
- [ ] 離線類別可單獨重現：`--only candles`、`--only cases`、`--only concepts`
- [ ] 技術指標資料不足時有 **warning**（非靜默跳過），既有檔案保留
- [ ] 每個 SVG 含 `<svg` 與 `</svg>`、`viewBox`、非空 `aria-label`

### Phase B — 引用完整性（每次改 Markdown 後）

- [ ] 所有 Markdown 圖片引用路徑對應到實際檔案（`uv run pytest tests/ -k images`）
- [ ] 教學 SVG 至少被一篇 Markdown 引用（`logo.svg` 除外）
- [ ] `uv run mkdocs build --strict` 通過

### Phase C — Mermaid 語法與渲染

- [ ] 每個 ` ```mermaid ` 區塊有對應結尾 fence
- [ ] 節點 ID 無空格、不使用保留字（`end`、`subgraph` 等）
- [ ] `mkdocs build` 無 Mermaid 渲染錯誤

### Phase D — 內容與術語一致性

- [ ] K 線術語與 SVG `aria-label` 一致（紅K、黑K，K 前不空格，見 [寫作規範](STYLE-GUIDE.md)）
- [ ] 案例頁符合模板：背景 → 表/圖 → Mermaid 推理 → 結論 → 反思
- [ ] 圖表專章描述的圖表類型，至少有 SVG 示意或 Mermaid 流程其一

### Phase E — 分類覆蓋度（季度審查）

- [ ] 八大圖表分類各有至少 1 張 SVG
- [ ] 所有實戰案例頁均含視覺元素（SVG 或 Mermaid）

---

## 自動化驗證

`tests/` 以 pytest 覆蓋 Phase A/B 的可程式化部分：

```bash
uv run pytest tests/ -v
```

| 測試 | 對應 Phase |
|------|-----------|
| 產生器檔名集合 == 預期清單 | A |
| 每張 SVG well-formed（`<svg>`/`viewBox`/`aria-label`） | A |
| Markdown 圖片連結皆存在 | B |
| 教學 SVG 皆被引用 | B |
| 指標資料不足時發出 warning | A |
| 指標公式（SMA/EMA/RSI/MACD） | A |

CI 於 `mkdocs build --strict` 前先跑 `pytest`，見 [`.github/workflows/deploy-docs.yml`](https://github.com/stock-school)。
