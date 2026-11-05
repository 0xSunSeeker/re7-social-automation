#!/usr/bin/env python3
"""Re7 social automation. One command: python run.py"""
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv

import ai
import analyse
import collect
import config
import create
import output


def main():
    load_dotenv()
    run_id = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    run_dir = Path("runs") / run_id
    ai.setup(run_dir / "ai")  # stops here if there is no API key

    print("1/4 Collecting")
    posts, sources = collect.collect()
    cov = collect.coverage(posts)
    for c in cov:
        print(f"    {c['entity']:8} {c['channel']:9} {c['captured']:3} posts  ({c['source']})")
    print(f"    {len(sources)} sources: " + " | ".join(s["title"][:50] for s in sources))

    print("2/4 Analysing (Claude labels themes, Python ranks)")
    analyse.classify(posts)
    analyse.score(posts)
    table = analyse.groups(posts)
    summary = analyse.channel_summary(posts)
    findings = analyse.findings(table, summary)
    for i, f in enumerate(findings, 1):
        print(f"    {i}. {f['headline']}")

    print("3/4 Creating drafts")
    drafts = create.generate(findings, sources)

    print("4/4 Writing outputs")
    meta = {"run_id": run_id, "model": config.MODEL, "ai_calls": ai._counter, "posts": len(posts), "sources": len(sources)}
    output.save_data(run_dir, posts, table, sources, drafts)
    output.write_markdown(run_dir, meta, cov, summary, table, findings, drafts)
    output.write_pdf(run_dir / "report.pdf", meta, cov, summary, table, findings, drafts)
    shutil.copy(run_dir / "report.pdf", "report.pdf")
    shutil.copy(run_dir / "report.md", "report.md")
    print(f"Done. {run_dir}/ and report.pdf")


if __name__ == "__main__":
    try:
        main()
    except (collect.CollectError, ai.AIError) as e:
        print(f"\nSTOPPED: {e}", file=sys.stderr)
        sys.exit(1)
