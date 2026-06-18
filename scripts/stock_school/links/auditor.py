"""Orchestrate link checks and render reports (SRP + OCP).

新增檢查器只需實作 ``run(ctx) -> list[Issue]`` 並加入 ``DEFAULT_CHECKS``，
無需修改 ``LinkAuditor`` 本體（OCP）。
"""
from __future__ import annotations

import datetime as _dt
from collections import Counter
from pathlib import Path
from typing import Protocol

import yaml

from stock_school.links.models import AuditContext, Document, Issue, Severity
from stock_school.links.reachability import ExternalLinkCheck, ReachabilityCheck
from stock_school.links.scanner import load_document
from stock_school.links.semantic import (
    CanonicalComplianceCheck,
    DictionaryAlignmentCheck,
    NavTitleConsistencyCheck,
)


class Check(Protocol):
    def run(self, ctx: AuditContext) -> list[Issue]: ...


DEFAULT_CHECKS: list[Check] = [
    ReachabilityCheck(),
    ExternalLinkCheck(),
    DictionaryAlignmentCheck(),
    CanonicalComplianceCheck(),
    NavTitleConsistencyCheck(),
]


class _IgnoreUnknownTagsLoader(yaml.SafeLoader):
    """讓 yaml 略過 mkdocs.yml 中的 ``!!python/name:`` 等自訂標籤。"""


def _ignore_unknown(loader: yaml.Loader, suffix: str, node: yaml.Node):  # noqa: ARG001
    return None


_IgnoreUnknownTagsLoader.add_multi_constructor("", _ignore_unknown)
_IgnoreUnknownTagsLoader.add_multi_constructor("tag:yaml.org,2002:python/name:", _ignore_unknown)


def _walk_nav(node, titles: dict[str, str]) -> None:
    if isinstance(node, list):
        for item in node:
            _walk_nav(item, titles)
    elif isinstance(node, dict):
        for key, value in node.items():
            if isinstance(value, str) and value.endswith(".md"):
                titles[value] = str(key)
            else:
                _walk_nav(value, titles)


def _parse_nav_titles(mkdocs_yml: Path) -> dict[str, str]:
    if not mkdocs_yml.exists():
        return {}
    data = yaml.load(mkdocs_yml.read_text(encoding="utf-8"), Loader=_IgnoreUnknownTagsLoader)
    titles: dict[str, str] = {}
    _walk_nav((data or {}).get("nav", []), titles)
    return titles


class LinkAuditor:
    """掃描文件、執行檢查、彙整問題。"""

    def __init__(self, repo_root: Path, *, checks: list[Check] | None = None) -> None:
        self._repo_root = repo_root
        self._checks = checks if checks is not None else DEFAULT_CHECKS

    def discover_documents(self) -> dict[str, Document]:
        docs: dict[str, Document] = {}
        paths = sorted((self._repo_root / "docs").rglob("*.md"))
        readme = self._repo_root / "README.md"
        if readme.exists():
            paths.append(readme)
        for path in paths:
            doc = load_document(self._repo_root, path)
            docs[doc.relpath] = doc
        return docs

    def audit(self, *, check_external: bool = False) -> tuple[list[Issue], AuditContext]:
        ctx = AuditContext(
            repo_root=self._repo_root,
            documents=self.discover_documents(),
            nav_titles=_parse_nav_titles(self._repo_root / "mkdocs.yml"),
            check_external=check_external,
        )
        issues: list[Issue] = []
        for check in self._checks:
            issues.extend(check.run(ctx))
        issues.sort(key=lambda i: (i.severity.value, i.source, i.line))
        return issues, ctx


def summarize(issues: list[Issue]) -> Counter:
    return Counter(issue.severity for issue in issues)


def render_report(issues: list[Issue], ctx: AuditContext) -> str:
    counts = summarize(issues)
    total_links = sum(len(doc.links) for doc in ctx.documents.values())
    today = _dt.date.today().isoformat()
    lines = [
        "# 連結稽核報告",
        "",
        f"- 產生日期：{today}",
        f"- 掃描檔案：{len(ctx.documents)} 篇",
        f"- 連結總數：{total_links} 條",
        f"- 外部連線檢查：{'啟用' if ctx.check_external else '未啟用'}",
        "",
        "## 問題統計",
        "",
        "| 嚴重度 | 數量 |",
        "|--------|------|",
        f"| error | {counts.get(Severity.ERROR, 0)} |",
        f"| warning | {counts.get(Severity.WARNING, 0)} |",
        f"| info | {counts.get(Severity.INFO, 0)} |",
        "",
    ]
    if not issues:
        lines.append("無發現問題，所有連結與錨點均可解析。")
        return "\n".join(lines) + "\n"

    lines += [
        "## 問題明細",
        "",
        "| 嚴重度 | 類型 | 位置 | 連結文字 | href | 說明 |",
        "|--------|------|------|----------|------|------|",
    ]
    lines += [issue.as_row() for issue in issues]
    lines.append("")
    return "\n".join(lines) + "\n"
