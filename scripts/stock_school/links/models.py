"""Immutable data models for the link audit (SRP)."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path


class Severity(Enum):
    """問題嚴重度。ERROR 會讓 ``--strict`` 失敗；其餘僅供人工檢視。"""

    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


class LinkKind(Enum):
    """連結分類，對應計畫的連結類型。"""

    INTERNAL = "internal"   # 站內 .md 檔（可帶錨點）
    ANCHOR = "anchor"       # 純錨點（#fragment，指向同頁）
    IMAGE = "image"         # 圖片資源
    ASSET = "asset"         # 其他站內非 .md 檔（如 .yml、.svg 連結）
    EXTERNAL = "external"   # http(s) / mailto / tel


@dataclass(frozen=True)
class Link:
    """單一 Markdown 連結，保留來源位置以利定位。"""

    source: str          # 來源檔（相對 repo 根、posix 路徑）
    line: int
    text: str            # 顯示文字（已去除前後空白）
    href: str            # 原始 href
    is_image: bool
    kind: LinkKind
    target_path: str     # href 中 ``#`` 之前的路徑部分（純錨點時為空字串）
    anchor: str | None   # ``#`` 之後的片段；無錨點為 None


@dataclass(frozen=True)
class Issue:
    """一筆檢查結果。"""

    severity: Severity
    kind: str            # 問題類型代碼，如 ``missing-file``、``broken-anchor``
    source: str
    line: int
    message: str
    link_text: str = ""
    href: str = ""

    def as_row(self) -> str:
        loc = f"{self.source}:{self.line}"
        text = self.link_text.replace("|", "\\|")
        href = self.href.replace("|", "\\|")
        msg = self.message.replace("|", "\\|")
        return f"| {self.severity.value} | {self.kind} | {loc} | {text} | {href} | {msg} |"


@dataclass
class Document:
    """一篇已解析的 Markdown 文件。"""

    relpath: str                 # 相對 repo 根，posix 路徑
    abspath: Path
    text: str
    links: list[Link] = field(default_factory=list)
    anchors: dict[str, str] = field(default_factory=dict)  # id -> 標題文字
    title: str = ""              # H1 文字（無則為空）


@dataclass
class AuditContext:
    """各檢查器共用的稽核上下文。"""

    repo_root: Path
    documents: dict[str, Document]   # key = relpath
    nav_titles: dict[str, str]       # docs 相對路徑 -> nav 顯式標題
    check_external: bool = False
