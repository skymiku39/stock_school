"""L3/L4 checks: link-text semantics and canonical compliance (SRP).

這些檢查屬「啟發式」，輸出多為 INFO/WARNING，標記待人工確認，
不應讓建置失敗（只有 L1/L2 的 ERROR 會）。
"""
from __future__ import annotations

import posixpath
import re
from urllib.parse import unquote

from stock_school.links.models import AuditContext, Issue, Link, LinkKind, Severity

_CJK_RE = re.compile(r"[\u4e00-\u9fff]")
_DICTIONARY = "docs/02-glossary/dictionary.md"
# 詞典表格列：| 術語 | 定義 | [文字](href) |
_DICT_ROW_RE = re.compile(r"^\|\s*([^|]+?)\s*\|")


def _resolve(source_relpath: str, target_path: str) -> str:
    base = posixpath.dirname(source_relpath)
    return posixpath.normpath(posixpath.join(base, target_path))


def _cjk_chars(text: str) -> set[str]:
    return set(_CJK_RE.findall(text))


class DictionaryAlignmentCheck:
    """L3：詞典每列「術語」應與其延伸連結的目標小節語意相關。

    僅檢查 dictionary.md 中帶錨點的連結，比對該列術語與目標小節標題是否
    有共同中文字；無共同字代表詞條可能連錯小節，標記 INFO 待人工確認。
    """

    def run(self, ctx: AuditContext) -> list[Issue]:
        doc = ctx.documents.get(_DICTIONARY)
        if doc is None:
            return []
        terms = self._terms_by_line(doc.text)
        issues: list[Issue] = []
        for link in doc.links:
            if link.kind is not LinkKind.INTERNAL or not link.anchor:
                continue
            term = terms.get(link.line)
            if not term:
                continue
            target = _resolve(link.source, unquote(link.target_path))
            target_doc = ctx.documents.get(target)
            if target_doc is None:
                continue
            heading = target_doc.anchors.get(unquote(link.anchor))
            if not heading:
                continue
            term_cjk = _cjk_chars(term)
            head_cjk = _cjk_chars(heading)
            if not term_cjk or not head_cjk or (term_cjk & head_cjk):
                continue
            issues.append(
                Issue(
                    Severity.INFO,
                    "dict-anchor-mismatch",
                    link.source,
                    link.line,
                    f"詞條「{term}」連向小節「{heading}」，兩者無共同字，請確認錨點是否正確",
                    link.text,
                    link.href,
                )
            )
        return issues

    @staticmethod
    def _terms_by_line(text: str) -> dict[int, str]:
        terms: dict[int, str] = {}
        for lineno, raw in enumerate(text.splitlines(), start=1):
            m = _DICT_ROW_RE.match(raw)
            if not m:
                continue
            term = m.group(1).strip().strip("*").strip()
            # 略過表頭與分隔列
            if not term or set(term) <= set("-: ") or term in {"術語", "名詞", "用語"}:
                continue
            terms[lineno] = term
        return terms


class CanonicalComplianceCheck:
    """L4：特定主題不應連向 ARCHITECTURE.md 標記為「只摘要」的頁面。

    依架構對照表，某些頁面僅應摘要並連向權威章節，不該被當成該主題的
    詳解來源。此檢查精準偵測這類反模式（連向摘要頁），作為回歸防護。
    """

    # 主題關鍵字 -> (權威章節, 禁止當詳解來源的摘要頁集合)
    _RULES: dict[str, tuple[str, set[str]]] = {
        "定期定額": ("docs/08-investing/etf-passive-dca.md", {"docs/01-basics/etf-intro.md"}),
        "三層費用": (
            "docs/01-basics/etf-costs-and-premium.md",
            {"docs/06-risk/trading-costs.md"},
        ),
        "收益平準金": (
            "docs/01-basics/etf-costs-and-premium.md",
            {"docs/06-risk/trading-costs.md", "docs/08-investing/etf-high-dividend.md"},
        ),
    }

    def run(self, ctx: AuditContext) -> list[Issue]:
        issues: list[Issue] = []
        for doc in ctx.documents.values():
            for link in doc.links:
                if link.kind is not LinkKind.INTERNAL:
                    continue
                issue = self._check(link)
                if issue is not None:
                    issues.append(issue)
        return issues

    def _check(self, link: Link) -> Issue | None:
        target = _resolve(link.source, unquote(link.target_path))
        for keyword, (canonical, summary_pages) in self._RULES.items():
            if keyword in link.text and target in summary_pages:
                return Issue(
                    Severity.WARNING,
                    "canonical-mismatch",
                    link.source,
                    link.line,
                    f"「{keyword}」的詳解應連向 {canonical}，不應連向摘要頁 {target}",
                    link.text,
                    link.href,
                )
        return None


class NavTitleConsistencyCheck:
    """L3：mkdocs.yml 的顯式 nav 標題與頁面 H1 應語意一致。"""

    def run(self, ctx: AuditContext) -> list[Issue]:
        issues: list[Issue] = []
        for docs_relpath, nav_title in ctx.nav_titles.items():
            relpath = f"docs/{docs_relpath}"
            # 首頁標籤為慣用結構名稱，與站名不需字面重疊
            if relpath == "docs/index.md":
                continue
            doc = ctx.documents.get(relpath)
            if doc is None or not doc.title:
                continue
            nav_cjk = _cjk_chars(nav_title)
            h1_cjk = _cjk_chars(doc.title)
            if not nav_cjk or not h1_cjk or (nav_cjk & h1_cjk):
                continue
            issues.append(
                Issue(
                    Severity.INFO,
                    "nav-h1-mismatch",
                    relpath,
                    1,
                    f"nav 標題「{nav_title}」與頁面 H1「{doc.title}」無共同字，請確認",
                    nav_title,
                    relpath,
                )
            )
        return issues
