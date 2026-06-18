"""Audit Markdown hyperlinks: file existence, anchors, text semantics, canonical.

用法：
    uv run python scripts/check_links.py                  # 全站稽核，列印摘要
    uv run python scripts/check_links.py --strict         # 有 ERROR 則離開碼為 1
    uv run python scripts/check_links.py --report out.md  # 另存 Markdown 報告
    uv run python scripts/check_links.py --check-external  # 一併檢查外部 URL
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from stock_school.links.auditor import LinkAuditor, render_report, summarize
from stock_school.links.models import Severity

REPO_ROOT = Path(__file__).resolve().parent.parent


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Stock School 連結稽核工具")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="發現 ERROR（斷檔／斷錨點）時回傳非零離開碼",
    )
    parser.add_argument(
        "--report",
        type=Path,
        help="將 Markdown 報告寫入指定路徑",
    )
    parser.add_argument(
        "--check-external",
        action="store_true",
        help="以網路請求驗證外部 URL（較慢，可能受網路波動影響）",
    )
    args = parser.parse_args(argv)

    auditor = LinkAuditor(REPO_ROOT)
    issues, ctx = auditor.audit(check_external=args.check_external)
    counts = summarize(issues)

    errors = counts.get(Severity.ERROR, 0)
    warnings = counts.get(Severity.WARNING, 0)
    infos = counts.get(Severity.INFO, 0)
    total_links = sum(len(doc.links) for doc in ctx.documents.values())

    print(f"掃描 {len(ctx.documents)} 篇文件、{total_links} 條連結")
    print(f"ERROR={errors}  WARNING={warnings}  INFO={infos}")

    for issue in issues:
        if issue.severity is Severity.ERROR:
            print(f"  [ERROR] {issue.source}:{issue.line} {issue.kind} — {issue.message}")

    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(render_report(issues, ctx), encoding="utf-8")
        print(f"報告已寫入：{args.report}")

    if args.strict and errors:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
