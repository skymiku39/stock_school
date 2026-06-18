"""Link audit toolkit — scan Markdown links and validate reachability/semantics.

分層（SRP / OCP）：

- ``models``       — 連結、問題等不可變資料模型
- ``scanner``      — 從 Markdown 擷取連結與標題錨點
- ``reachability`` — L1/L2：檔案存在與錨點解析（錯誤級，必修）
- ``semantic``     — L3/L4：連結文字語意與 canonical 合規（提示級，待人工確認）
- ``auditor``      — 組裝各檢查器並輸出報告
"""
from __future__ import annotations
