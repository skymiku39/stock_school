"""L1/L2 checks: file existence and anchor resolution (SRP)."""
from __future__ import annotations

import posixpath
import urllib.error
import urllib.request
from urllib.parse import unquote

from stock_school.links.models import AuditContext, Issue, Link, LinkKind, Severity


def _resolve(source_relpath: str, target_path: str) -> str:
    """將相對 href 解析為相對 repo 根的 posix 路徑。"""
    base = posixpath.dirname(source_relpath)
    return posixpath.normpath(posixpath.join(base, target_path))


class ReachabilityCheck:
    """檢查站內連結目標檔與錨點是否存在。"""

    def run(self, ctx: AuditContext) -> list[Issue]:
        issues: list[Issue] = []
        for doc in ctx.documents.values():
            for link in doc.links:
                issues.extend(self._check_link(ctx, link))
        return issues

    def _check_link(self, ctx: AuditContext, link: Link) -> list[Issue]:
        if link.kind is LinkKind.EXTERNAL:
            return []
        if link.kind is LinkKind.ANCHOR:
            return self._check_anchor(ctx, link, link.source)
        if link.kind in (LinkKind.IMAGE, LinkKind.ASSET):
            return self._check_asset(ctx, link)
        return self._check_internal(ctx, link)

    def _check_internal(self, ctx: AuditContext, link: Link) -> list[Issue]:
        target = _resolve(link.source, unquote(link.target_path))
        doc = ctx.documents.get(target)
        if doc is None:
            return [
                Issue(
                    Severity.ERROR,
                    "missing-file",
                    link.source,
                    link.line,
                    f"連結目標檔不存在：{target}",
                    link.text,
                    link.href,
                )
            ]
        if link.anchor:
            return self._check_anchor(ctx, link, target)
        return []

    def _check_anchor(self, ctx: AuditContext, link: Link, target_relpath: str) -> list[Issue]:
        if not link.anchor:
            return []
        doc = ctx.documents.get(target_relpath)
        if doc is None:
            return []  # 目標檔缺失已在他處回報
        anchor = unquote(link.anchor)
        if anchor not in doc.anchors:
            return [
                Issue(
                    Severity.ERROR,
                    "broken-anchor",
                    link.source,
                    link.line,
                    f"錨點不存在：{target_relpath}#{anchor}",
                    link.text,
                    link.href,
                )
            ]
        return []

    def _check_asset(self, ctx: AuditContext, link: Link) -> list[Issue]:
        target = _resolve(link.source, unquote(link.target_path))
        if not (ctx.repo_root / target).exists():
            kind = "missing-image" if link.kind is LinkKind.IMAGE else "missing-asset"
            return [
                Issue(
                    Severity.ERROR,
                    kind,
                    link.source,
                    link.line,
                    f"資源檔不存在：{target}",
                    link.text,
                    link.href,
                )
            ]
        return []


class ExternalLinkCheck:
    """以網路請求檢查外部 URL（僅在 ``--check-external`` 時啟用）。"""

    def __init__(self, *, timeout: float = 10.0) -> None:
        self._timeout = timeout

    def run(self, ctx: AuditContext) -> list[Issue]:
        if not ctx.check_external:
            return []
        issues: list[Issue] = []
        seen: dict[str, str | None] = {}
        for doc in ctx.documents.values():
            for link in doc.links:
                if link.kind is not LinkKind.EXTERNAL or not link.href.lower().startswith("http"):
                    continue
                error = seen.get(link.href, "__missing__")
                if error == "__missing__":
                    error = self._probe(link.href)
                    seen[link.href] = error
                if error is not None:
                    issues.append(
                        Issue(
                            Severity.WARNING,
                            "external-unreachable",
                            link.source,
                            link.line,
                            f"外部連結無法連線（{error}）：{link.href}",
                            link.text,
                            link.href,
                        )
                    )
        return issues

    def _probe(self, url: str) -> str | None:
        request = urllib.request.Request(
            url, method="HEAD", headers={"User-Agent": "stock-school-link-audit"}
        )
        try:
            with urllib.request.urlopen(request, timeout=self._timeout) as resp:
                return None if resp.status < 400 else f"HTTP {resp.status}"
        except urllib.error.HTTPError as exc:  # noqa: PERF203 - 少量 URL，可接受
            # 部分網站拒絕 HEAD，改試 GET
            if exc.code in (403, 405):
                return self._probe_get(url)
            return f"HTTP {exc.code}"
        except (urllib.error.URLError, OSError) as exc:
            return str(getattr(exc, "reason", exc))

    def _probe_get(self, url: str) -> str | None:
        request = urllib.request.Request(
            url, method="GET", headers={"User-Agent": "stock-school-link-audit"}
        )
        try:
            with urllib.request.urlopen(request, timeout=self._timeout) as resp:
                return None if resp.status < 400 else f"HTTP {resp.status}"
        except urllib.error.HTTPError as exc:
            return f"HTTP {exc.code}"
        except (urllib.error.URLError, OSError) as exc:
            return str(getattr(exc, "reason", exc))
