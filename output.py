"""Output: one folder per run with the data, the AI logs, report.md and report.pdf."""
import csv
import json
import re
import sqlite3
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import config

POST_FIELDS = ["entity", "channel", "post_id", "date", "date_display", "text", "format", "ai_format", "theme",
               "likes", "comments", "reposts", "views", "metric", "percentile", "excluded", "url", "source"]
REPO_URL = "https://github.com/0xSunSeeker/re7-social-automation"


def save_data(run_dir, posts, table, sources, drafts):
    with open(run_dir / "posts.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=POST_FIELDS, extrasaction="ignore")
        w.writeheader()
        w.writerows(posts)
    with open(run_dir / "performance.csv", "w", newline="", encoding="utf-8") as f:
        fields = ["entity", "channel", "theme", "format", "n", "metric", "median", "median_percentile", "status"]
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(table)
    (run_dir / "sources.json").write_text(json.dumps(sources, indent=2, ensure_ascii=False))
    (run_dir / "drafts.json").write_text(json.dumps(drafts, indent=2, ensure_ascii=False))
    db = sqlite3.connect(run_dir / "re7.sqlite")
    db.execute(f"CREATE TABLE posts ({', '.join(POST_FIELDS)})")
    db.executemany(f"INSERT INTO posts VALUES ({', '.join('?' * len(POST_FIELDS))})",
                   [[p.get(k) for k in POST_FIELDS] for p in posts])
    db.execute("CREATE TABLE performance (entity, channel, theme, format, n, metric, median, median_percentile, status)")
    db.executemany("INSERT INTO performance VALUES (?,?,?,?,?,?,?,?,?)",
                   [[r[k] for k in ("entity", "channel", "theme", "format", "n", "metric", "median",
                                    "median_percentile", "status")] for r in table])
    db.commit()
    db.close()


def fmt_num(v):
    if v is None:
        return "-"
    return f"{v:,.0f}" if float(v).is_integer() else f"{v:,.1f}"


def write_markdown(run_dir, meta, cov, summary, table, findings, drafts):
    L = [f"# Re7 social automation: run {meta['run_id']}", "",
         f"Model: `{meta['model']}` · {meta['ai_calls']} logged API calls in `ai/` · {meta['posts']} posts · "
         f"{meta['sources']} sources", "", "## Coverage", "",
         "| Entity | Channel | Posts | With metric | How |", "|---|---|---:|---:|---|"]
    L += [f"| {c['entity']} | {c['channel']} | {c['captured']} | {c['with_metric']} | {c['source']} |" for c in cov]
    L += ["", "## Channel baselines (ranked posts only)", "", "| Entity | Channel | Metric | n | Median | Min | Max |",
          "|---|---|---|---:|---:|---:|---:|"]
    L += [f"| {s['entity']} | {s['channel']} | {s['metric']} | {s['n']} | {fmt_num(s['median'])} | {fmt_num(s['min'])} | "
          f"{fmt_num(s['max'])} |" for s in summary]
    L += ["", "## Theme x format", "", "| Entity | Channel | Theme | Format | n | Median | Median pct | Status |",
          "|---|---|---|---|---:|---:|---:|---|"]
    L += [f"| {r['entity']} | {r['channel']} | {r['theme']} | {r['format']} | {r['n']} | {fmt_num(r['median'])} "
          f"{r['metric']} | {fmt_num(r['median_percentile'])} | {r['status']} |" for r in table]
    L += ["", "## Findings", ""]
    for i, f in enumerate(findings, 1):
        L += [f"**{i}. {f['headline']}**  ", f"{f['detail']}  ", f"*Action:* {f['action']}", ""]
    L += ["## Drafts", ""]
    for i, d in enumerate(drafts, 1):
        L += [f"### {i}. {d['entity']} · {d['channel']} · finding {d['finding_used']}", "",
              *[f"> {line}" if line else ">" for line in d["final_text"].split("\n")], "",
              f"Format: {d['format_brief']}  ", f"Why: {d['why']}  ", f"Source: [{d['source_title']}]({d['source_url']})", ""]
    (run_dir / "report.md").write_text("\n".join(L), encoding="utf-8")


# ---------- PDF ----------

NON_BMP = re.compile("[\U00010000-\U0010FFFF☀-➿️]")
INK, MUTED, LINE, ACCENT = colors.HexColor("#1a1a1a"), colors.HexColor("#666666"), colors.HexColor("#d9d9d9"), colors.HexColor("#0b3d2e")


def P(text, style):
    return Paragraph(escape(NON_BMP.sub("", text)).replace("\n", "<br/>"), style)


def write_pdf(path, meta, cov, summary, table, findings, drafts):
    ss = getSampleStyleSheet()
    body = ParagraphStyle("b", parent=ss["Normal"], fontName="Helvetica", fontSize=9.5, leading=13.5, textColor=INK, spaceAfter=6)
    small = ParagraphStyle("s", parent=body, fontSize=8, leading=10.5, textColor=MUTED, spaceAfter=0)
    cell = ParagraphStyle("c", parent=body, fontSize=8, leading=10, spaceAfter=0)
    h1 = ParagraphStyle("h1", parent=body, fontName="Helvetica-Bold", fontSize=17, leading=21, spaceAfter=4)
    h2 = ParagraphStyle("h2", parent=body, fontName="Helvetica-Bold", fontSize=11.5, leading=15, spaceBefore=8, spaceAfter=5, textColor=ACCENT)
    bold = ParagraphStyle("bd", parent=body, fontName="Helvetica-Bold", spaceAfter=2)
    mono = ParagraphStyle("m", parent=body, fontName="Courier", fontSize=8.5, leading=11, backColor=colors.HexColor("#f4f4f4"), borderPadding=5, spaceBefore=4, spaceAfter=10)
    quote = ParagraphStyle("q", parent=body, fontSize=8.5, leading=11.5, leftIndent=8, borderColor=LINE, borderWidth=0, spaceAfter=3)

    def grid(rows, widths, header=True):
        t = Table([[c if not isinstance(c, str) else P(c, cell) for c in r] for r in rows], colWidths=widths, repeatRows=1)
        style = [("LINEBELOW", (0, 0), (-1, -1), 0.4, LINE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                 ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]
        if header:
            style += [("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#eef3f1")), ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold")]
        t.setStyle(TableStyle(style))
        return t

    s = []
    # Page 1
    s += [P("Re7 social automation", h1),
          P(f"Analyst, Investor Relations & Marketing task · Ayman Zahran · run {meta['run_id']}", small), Spacer(1, 10),
          P("One command pulls Re7's recent posts from X, LinkedIn and Telegram into a single table, has Claude label "
            "every post by theme and format, ranks what performs best on each channel, and then has Claude write new "
            "posts from Re7's own research using those results.", body)]
    boxes = [["COLLECT", "ANALYSE", "CREATE", "OUTPUT"],
             ["Telegram scraped live\nX and LinkedIn from CSV\nRe7 Research RSS and website",
              "Claude labels themes\nPython ranks per channel\nClaude writes findings",
              "Claude drafts 9 posts\nfrom real Re7 sources\nCode checks every one",
              "CSV, SQLite, report\nEvery API call logged"]]
    diag = Table([[P(c, ParagraphStyle("d", parent=cell, fontName="Helvetica-Bold", alignment=1, textColor=colors.white)) for c in boxes[0]],
                  [P(c, ParagraphStyle("d2", parent=cell, alignment=1)) for c in boxes[1]]], colWidths=[42 * mm] * 4)
    diag.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), ACCENT), ("BOX", (0, 0), (-1, -1), 0.6, ACCENT),
                              ("INNERGRID", (0, 0), (-1, -1), 0.6, colors.white), ("BACKGROUND", (0, 1), (-1, 1), colors.HexColor("#eef3f1")),
                              ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    s += [Spacer(1, 4), diag, Spacer(1, 10), P("How to run", h2),
          Paragraph("pip install -r requirements.txt<br/>echo 'ANTHROPIC_API_KEY=...' &gt; .env<br/>python run.py", mono),
          P(f"Each run writes a new folder under runs/. This run used {meta['model']} and made {meta['ai_calls']} API calls; "
            "the full request and response for each one is saved in ai/, so nothing in the findings or drafts was written by hand. "
            "If a source can't be fetched, a CSV is missing or the model's output fails a check twice, the run stops. "
            "There is no sample data and no fallback copy.", body),
          P("Design choices", h2),
          P("Each channel is ranked on its own metric: views on X and Telegram, reactions on LinkedIn. Numbers are never "
            "compared across channels or between Capital and Labs, because the audiences are different sizes. Posts are "
            "scored by percentile within their own entity and channel, so a Labs X post is only compared with other Labs X posts. "
            "Pinned posts, thread continuations, self-reposts and anything under 48 hours old are kept in the data but left out of rankings. "
            f"A theme and format combination needs at least {config.MIN_GROUP} posts before it counts as a pattern.", body),
          PageBreak()]

    # Page 2
    s += [P("What was collected", h1), Spacer(1, 4),
          grid([["Entity", "Channel", "Posts", "With metric", "Method"]] +
               [[c["entity"], c["channel"], str(c["captured"]), str(c["with_metric"]), c["source"]] for c in cov],
               [22 * mm, 22 * mm, 16 * mm, 22 * mm, 86 * mm]),
          Spacer(1, 6),
          P("Telegram is scraped live from the public channel preview. I don't have API access to Re7's X or LinkedIn, and "
            "scraping LinkedIn breaks its terms, so those posts come in as CSV. For this run I built the CSVs from screenshots "
            "of each feed. In production the same import takes an X API pull or a LinkedIn page analytics export with no code changes. "
            "LinkedIn screenshots only show relative dates such as '3w', so those stay as shown rather than being turned into fake timestamps. "
            "I couldn't find a public Re7 Capital Telegram channel, so that row is empty.", body),
          P("Baseline per channel (ranked posts only)", h2),
          grid([["Entity", "Channel", "Metric", "n", "Median", "Range"]] +
               [[r["entity"], r["channel"], r["metric"], str(r["n"]), fmt_num(r["median"]), f"{fmt_num(r['min'])} to {fmt_num(r['max'])}"] for r in summary],
               [22 * mm, 22 * mm, 24 * mm, 14 * mm, 22 * mm, 64 * mm]),
          P("Best theme and format combinations", h2)]
    ok = [r for r in table if r["status"] == "ok"]
    s += [grid([["Entity", "Channel", "Theme", "Format", "n", "Median", "Median pct"]] +
               [[r["entity"], r["channel"], r["theme"], r["format"], str(r["n"]), f"{fmt_num(r['median'])} {r['metric']}",
                 fmt_num(r["median_percentile"])] for r in ok],
               [18 * mm, 18 * mm, 38 * mm, 28 * mm, 10 * mm, 30 * mm, 26 * mm]),
          P(f"Only groups with at least {config.MIN_GROUP} posts are shown. The full table, including smaller groups, is in performance.csv.", small),
          PageBreak()]

    # Page 3
    s += [P("What the data says", h1)]
    for i, f in enumerate(findings, 1):
        s += [P(f"{i}. {f['headline']}", bold), P(f["detail"], body), P("Action: " + f["action"], ParagraphStyle("a", parent=body, textColor=ACCENT))]
    s += [PageBreak(), P("Drafts written from those findings", h1)]
    picks = []
    for channel, pick in (("X", min), ("LinkedIn", min), ("Telegram", min)):
        options = [d for d in drafts if d["channel"] == channel]
        if options:
            picks.append(pick(options, key=lambda d: len(d["text"])))
    for d in picks:
        s += [P(f"{d['entity']} · {d['channel']} · applies finding {d['finding_used']}", bold),
              P(d["final_text"], quote),
              P(f"Format: {d['format_brief']}. Source: {d['source_title']}", small), Spacer(1, 7)]
    s += [P("All nine drafts are in report.md and drafts.json.", small)]

    # Page 4
    lim = ParagraphStyle("l", parent=body, fontSize=8.5, leading=11.5, spaceAfter=3)
    s += [P("Limits", h2)]
    for b in ["X and LinkedIn numbers come from screenshots of each feed, not an analytics export. The LinkedIn feed was sorted by Top, so it leans towards posts that already did well.",
              "Views on X and Telegram measure reach. Reactions on LinkedIn measure engagement. Neither tells you about clicks, follows or allocator conversations.",
              "Small samples. The rankings show what has worked in this window, not what causes performance. Post age and subject still affect the numbers.",
              "The checks catch length, banned words, unsupported numbers and missing links. They can't judge whether a claim is still current, so every draft needs a human and compliance read before it goes out."]:
        s += [P("• " + b, lim)]
    s += [P("Next steps", h2)]
    for b in ["Swap the screenshot CSVs for the X API and a LinkedIn page analytics export. The importer already takes both.",
              "Run it weekly on a schedule and track whether the recommended formats actually move the medians.",
              "Add click data from Substack and the website, and send drafts to a review queue in Slack or Notion.",
              ]:
        s += [P("• " + b, lim)]
    s += [Spacer(1, 10), P(f"Code: {REPO_URL}", bold),
          P(f"Run {meta['run_id']} · model {meta['model']} · {meta['posts']} posts · {meta['sources']} sources · {meta['ai_calls']} logged API calls", small)]

    SimpleDocTemplate(str(path), pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=16 * mm,
                      bottomMargin=16 * mm, title="Re7 social automation", author="Ayman Zahran").build(s)
