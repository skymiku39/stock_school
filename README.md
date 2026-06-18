# Stock School — 台股教學

以 MkDocs 建置的台股靜態教學網站，可作**系統教材**或**基本資料書／字典**查閱：入門、100+ 詞條、看表、看圖、投資模式、老手專區與案例。

> **免責聲明**：本專案僅供教學與參考，不構成投資建議。實務交易請自行評估並承擔風險。

## 架構

SVG 產生器採 **SOLID** 分層與 **Publish/Subscribe** 事件匯流排（產圖與寫檔解耦）。詳見 [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)。

```bash
# 產生／更新教學用 SVG 圖表
uv run python scripts/generate_all.py
```

## 快速開始

```bash
cd stock_school
uv sync
uv run mkdocs serve
```

瀏覽器開啟 [http://127.0.0.1:8800](http://127.0.0.1:8800) 預覽。

> 預覽埠為 **8800**（設定於 `mkdocs.yml` 的 `dev_addr`），避免與 MkDocs 預設 8000 及相鄰 Stock Bot 儀表板 8501 衝突。臨時改用其他埠：`uv run mkdocs serve --dev-addr=127.0.0.1:9000`

## 建置靜態網站

```bash
uv run mkdocs build
```

輸出目錄為 `site/`，可部署至任意靜態主機。

## 部署至 GitHub Pages

專案已含 [`.github/workflows/deploy-docs.yml`](.github/workflows/deploy-docs.yml)：

1. 將 repo 推送到 GitHub。
2. 在 repo **Settings → Pages** 中，來源選 **GitHub Actions**。
3. 推送 `main` 或 `master` 分支後，workflow 會執行 `mkdocs gh-deploy`。
4. 網站發布至 `https://<username>.github.io/<repo>/`。

手動建置上傳：執行 `uv run mkdocs build`，將 `site/` 目錄部署至任意靜態主機。

## 當字典 / 工具書用

| 需求 | 頁面 |
|------|------|
| 查名詞 | [完整詞條總表](docs/02-glossary/dictionary.md) |
| 查公式 | [公式速查](docs/appendix/formulas.md) |
| 查稅費（試算用） | [稅費總覽](docs/appendix/taxes-for-costing.md) |
| 查縮寫 | [縮寫對照](docs/appendix/abbreviations.md) |
| 使用指南 | [基本資料書](docs/appendix/reference-book.md) |
| 對號入座 | [我是誰，該怎麼投？](docs/10-persona/index.md) |

站內搜尋框可全文檢索（支援中英文縮寫）。

## 學習路徑建議

| 對象 | 建議順序 |
|------|----------|
| 完全新手 | 入門 → [**對號入座**](docs/10-persona/index.md) → 投資模式 → 術語詞典 → 看表／看圖 → 風險與紀律 |
| 有基礎者 | 對號入座／投資模式 → 分析思維 → 實戰案例 |
| 老手進階 | **老手專區**（研究流程、組合、多週期、事件手冊）→ 附錄 |

## 內容規模（約）

- **約 120 篇** Markdown 章節
- **21 張** K 線 SVG（含 4 張組合型態）
- 涵蓋術語、看表、看圖、評分、風控、投資模式、對號入座、**12 篇**實戰案例

## 與 Stock Bot 的關係

本教學站為**獨立閱讀**，不依賴交易 Bot。若要用實作工具練習，請參考 [附錄：工具對照](docs/appendix/stock-tool-map.md) 與相鄰的 `stock` 專案。
