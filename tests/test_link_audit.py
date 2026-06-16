"""Unit tests for the link audit toolkit."""
from __future__ import annotations

from pathlib import Path

from stock_school.links.auditor import LinkAuditor, render_report
from stock_school.links.models import AuditContext, Document, LinkKind, Severity
from stock_school.links.reachability import ReachabilityCheck
from stock_school.links.scanner import extract_anchors, extract_links
from stock_school.links.semantic import (
    CanonicalComplianceCheck,
    DictionaryAlignmentCheck,
    NavTitleConsistencyCheck,
)

REPO_ROOT = Path(__file__).resolve().parent.parent


def _doc(relpath: str, text: str) -> Document:
    anchors, title = extract_anchors(text)
    return Document(
        relpath=relpath,
        abspath=Path(relpath),
        text=text,
        links=extract_links(relpath, text),
        anchors=anchors,
        title=title,
    )


def _ctx(*docs: Document, nav_titles: dict[str, str] | None = None) -> AuditContext:
    return AuditContext(
        repo_root=REPO_ROOT,
        documents={d.relpath: d for d in docs},
        nav_titles=nav_titles or {},
    )


# ---------------------------------------------------------------------------
# scanner
# ---------------------------------------------------------------------------

def test_extract_links_classifies_kinds():
    text = (
        "[內部](b.md) 與 [錨點](b.md#sec) 與 [同頁](#here)\n"
        "![圖](../assets/x.svg) 與 [外部](https://example.com) 與 [資源](data.yml)\n"
    )
    links = extract_links("docs/a.md", text)
    by_text = {link.text: link for link in links}

    assert by_text["內部"].kind is LinkKind.INTERNAL
    assert by_text["內部"].target_path == "b.md"
    assert by_text["內部"].anchor is None

    assert by_text["錨點"].anchor == "sec"
    assert by_text["同頁"].kind is LinkKind.ANCHOR
    assert by_text["同頁"].target_path == ""
    assert by_text["同頁"].anchor == "here"

    assert by_text["圖"].kind is LinkKind.IMAGE
    assert by_text["圖"].is_image is True
    assert by_text["外部"].kind is LinkKind.EXTERNAL
    assert by_text["資源"].kind is LinkKind.ASSET


def test_extract_links_skips_code_blocks_and_inline_code():
    text = (
        "真實 [連結](real.md)\n"
        "```\n"
        "[程式碼內](fake.md)\n"
        "```\n"
        "行內 `[行內碼](also-fake.md)` 結束\n"
    )
    hrefs = {link.href for link in extract_links("docs/a.md", text)}
    assert "real.md" in hrefs
    assert "fake.md" not in hrefs
    assert "also-fake.md" not in hrefs


def test_extract_anchors_handles_explicit_and_auto_ids():
    text = "# 主標題\n\n## 中文小節 {#自訂-id}\n\n## English Heading\n"
    anchors, title = extract_anchors(text)
    assert title == "主標題"
    assert anchors["自訂-id"] == "中文小節"
    assert "english-heading" in anchors


# ---------------------------------------------------------------------------
# reachability (L1/L2)
# ---------------------------------------------------------------------------

def test_reachability_flags_missing_file_and_broken_anchor():
    source = _doc(
        "docs/a.md",
        "[好](b.md#存在) [缺檔](missing.md) [壞錨](b.md#不存在)\n",
    )
    target = _doc("docs/b.md", "# B\n\n## 存在 {#存在}\n")
    issues = ReachabilityCheck().run(_ctx(source, target))
    kinds = {(i.kind, i.severity) for i in issues}

    assert ("missing-file", Severity.ERROR) in kinds
    assert ("broken-anchor", Severity.ERROR) in kinds
    # 「好」連結可解析，不應產生問題
    assert not any(i.href == "b.md#存在" for i in issues)


def test_reachability_resolves_relative_and_anchor_only():
    source = _doc(
        "docs/sub/a.md",
        "[上層](../b.md#sec) [本頁](#self)\n## Self {#self}\n",
    )
    target = _doc("docs/b.md", "# B\n## Sec {#sec}\n")
    issues = ReachabilityCheck().run(_ctx(source, target))
    assert issues == []


def test_reachability_flags_missing_image(tmp_path: Path):
    source = _doc("docs/a.md", "![缺圖](../assets/none.svg)\n")
    ctx = AuditContext(repo_root=tmp_path, documents={source.relpath: source}, nav_titles={})
    issues = ReachabilityCheck().run(ctx)
    assert any(i.kind == "missing-image" and i.severity is Severity.ERROR for i in issues)


# ---------------------------------------------------------------------------
# semantic (L3/L4)
# ---------------------------------------------------------------------------

def test_dictionary_alignment_flags_unrelated_anchor():
    dictionary = _doc(
        "docs/02-glossary/dictionary.md",
        "| 術語 | 一句話 | 詳見 |\n"
        "|------|--------|------|\n"
        "| 開高低收 | 四個價格 | [行情](q.md#開高低收) |\n"
        "| 軋空 | 空方被迫回補 | [行情](q.md#開高低收) |\n",
    )
    target = _doc("docs/02-glossary/q.md", "# Q\n## 開高低收 {#開高低收}\n")
    issues = DictionaryAlignmentCheck().run(_ctx(dictionary, target))

    # 「開高低收」與目標小節同名 → 不標記；「軋空」與「開高低收」無共同字 → 標記
    assert len(issues) == 1
    assert issues[0].kind == "dict-anchor-mismatch"
    assert issues[0].link_text == "行情"
    assert "軋空" in issues[0].message


def test_canonical_compliance_flags_summary_page_only():
    bad = _doc("docs/x.md", "[定期定額怎麼做](01-basics/etf-intro.md)\n")
    good = _doc("docs/y.md", "[定期定額怎麼做](08-investing/etf-passive-dca.md)\n")
    ctx = _ctx(bad, good)
    issues = CanonicalComplianceCheck().run(ctx)

    assert len(issues) == 1
    assert issues[0].source == "docs/x.md"
    assert issues[0].severity is Severity.WARNING
    assert issues[0].kind == "canonical-mismatch"


def test_nav_h1_consistency_skips_home_and_flags_mismatch():
    home = _doc("docs/index.md", "# Stock School — 台股教學\n")
    page = _doc("docs/foo.md", "# 完全不同的標題\n")
    ctx = _ctx(home, page, nav_titles={"index.md": "首頁", "foo.md": "另一個名字"})
    issues = NavTitleConsistencyCheck().run(ctx)

    assert all(i.source != "docs/index.md" for i in issues)
    assert any(i.source == "docs/foo.md" and i.kind == "nav-h1-mismatch" for i in issues)


# ---------------------------------------------------------------------------
# auditor end-to-end against the real docs
# ---------------------------------------------------------------------------

def test_real_docs_have_no_reachability_errors():
    """全站不得有斷檔或斷錨點（L1/L2 必過）。"""
    issues, _ = LinkAuditor(REPO_ROOT, checks=[ReachabilityCheck()]).audit()
    errors = [i for i in issues if i.severity is Severity.ERROR]
    assert errors == [], "\n".join(f"{i.source}:{i.line} {i.message}" for i in errors)


def test_render_report_contains_summary():
    issues, ctx = LinkAuditor(REPO_ROOT).audit()
    report = render_report(issues, ctx)
    assert "# 連結稽核報告" in report
    assert "問題統計" in report
