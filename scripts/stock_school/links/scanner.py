"""Extract links and heading anchors from Markdown (SRP)."""
from __future__ import annotations

import re
from pathlib import Path

import markdown

from stock_school.links.models import Document, Link, LinkKind

# [text](href) 與 ![alt](src)；href 取到空白或右括號前，並允許可選的 "title"
_LINK_RE = re.compile(r"(!?)\[([^\]]*)\]\(\s*([^)\s]+)(?:\s+\"[^\"]*\")?\s*\)")
_INLINE_CODE_RE = re.compile(r"`[^`]*`")
_FENCE_RE = re.compile(r"^\s*(```|~~~)")
_EXTERNAL_RE = re.compile(r"^(https?:|mailto:|tel:|//)", re.IGNORECASE)
_HEADING_HTML_RE = re.compile(r"<h([1-6])[^>]*\sid=\"([^\"]+)\"[^>]*>(.*?)</h\1>", re.DOTALL)
_TAG_RE = re.compile(r"<[^>]+>")

# 與 mkdocs.yml 盡量一致，確保標題 id 的產生方式（含 {#id} 與自動 slug）相符
_MD_EXTENSIONS = ["toc", "attr_list", "tables", "fenced_code", "md_in_html"]


def _classify(href: str, is_image: bool) -> tuple[LinkKind, str, str | None]:
    """回傳 (kind, target_path, anchor)。"""
    if _EXTERNAL_RE.match(href):
        return LinkKind.EXTERNAL, href, None

    target, _, anchor = href.partition("#")
    anchor = anchor or None

    if target == "":
        return LinkKind.ANCHOR, "", anchor
    if is_image:
        return LinkKind.IMAGE, target, anchor
    if target.lower().endswith(".md"):
        return LinkKind.INTERNAL, target, anchor
    return LinkKind.ASSET, target, anchor


def extract_links(source_relpath: str, text: str) -> list[Link]:
    """擷取連結，略過 fenced code 區塊與行內 code span。"""
    links: list[Link] = []
    in_fence = False
    for lineno, raw in enumerate(text.splitlines(), start=1):
        if _FENCE_RE.match(raw):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        line = _INLINE_CODE_RE.sub("", raw)
        for m in _LINK_RE.finditer(line):
            is_image = m.group(1) == "!"
            link_text = m.group(2).strip()
            href = m.group(3).strip()
            kind, target_path, anchor = _classify(href, is_image)
            links.append(
                Link(
                    source=source_relpath,
                    line=lineno,
                    text=link_text,
                    href=href,
                    is_image=is_image,
                    kind=kind,
                    target_path=target_path,
                    anchor=anchor,
                )
            )
    return links


def extract_anchors(text: str) -> tuple[dict[str, str], str]:
    """以 markdown 轉譯後抓取標題 id，回傳 (id->標題文字, H1 標題)。

    透過實際轉譯確保 ``{#自訂-id}`` 與自動 slug 的產生方式與站台一致。
    """
    md = markdown.Markdown(extensions=_MD_EXTENSIONS)
    html = md.convert(text)
    anchors: dict[str, str] = {}
    title = ""
    for m in _HEADING_HTML_RE.finditer(html):
        level, anchor_id, inner = int(m.group(1)), m.group(2), m.group(3)
        heading_text = _TAG_RE.sub("", inner).strip()
        anchors[anchor_id] = heading_text
        if level == 1 and not title:
            title = heading_text
    return anchors, title


def load_document(repo_root: Path, abspath: Path) -> Document:
    relpath = abspath.relative_to(repo_root).as_posix()
    text = abspath.read_text(encoding="utf-8")
    anchors, title = extract_anchors(text)
    return Document(
        relpath=relpath,
        abspath=abspath,
        text=text,
        links=extract_links(relpath, text),
        anchors=anchors,
        title=title,
    )
