"""Collect: Telegram scrape, X and LinkedIn imports, and the Re7 source library. No fallbacks, no sample data."""
import csv
import re
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

import requests
from bs4 import BeautifulSoup

import config

HEADERS = {"User-Agent": "re7-social-automation/1.0 (job application task)"}
FIELDS = ["entity", "channel", "post_id", "date", "date_display", "text", "format", "likes", "comments",
          "reposts", "views", "url", "source", "excluded"]


class CollectError(RuntimeError):
    pass


def parse_count(value):
    """'1.2K' -> 1200. Empty or unreadable -> None. Never turns missing into 0."""
    if value is None:
        return None
    v = str(value).strip().upper().replace(",", "")
    if not v:
        return None
    try:
        mult = 1
        if v.endswith("K"):
            mult, v = 1_000, v[:-1]
        elif v.endswith("M"):
            mult, v = 1_000_000, v[:-1]
        return int(round(float(v) * mult))
    except ValueError:
        return None


def is_true(value):
    return str(value).strip().lower() in ("true", "1", "yes")


def get(url):
    r = requests.get(url, headers=HEADERS, timeout=20)
    if r.status_code != 200:
        raise CollectError(f"{url} returned HTTP {r.status_code}")
    return r.text


# ---------- Telegram ----------

def parse_telegram(html, entity, channel):
    soup = BeautifulSoup(html, "html.parser")
    posts = []
    for msg in soup.select("div.tgme_widget_message"):
        post_id = msg.get("data-post")
        if not post_id:
            continue
        text_div = msg.select_one(".tgme_widget_message_text")
        time_tag = msg.select_one("time[datetime]")
        views = msg.select_one(".tgme_widget_message_views")
        if msg.select_one(".tgme_widget_message_video_player, .tgme_widget_message_roundvideo_player"):
            fmt = "video"
        elif msg.select_one(".tgme_widget_message_photo_wrap"):
            fmt = "image"
        elif msg.select_one(".tgme_widget_message_link_preview"):
            fmt = "link post"
        else:
            fmt = "text-only"
        posts.append({
            "entity": entity, "channel": "Telegram", "post_id": post_id,
            "date": time_tag["datetime"] if time_tag else None, "date_display": None,
            "text": text_div.get_text(" ", strip=True) if text_div else "",
            "format": fmt, "likes": None, "comments": None, "reposts": None,
            "views": parse_count(views.get_text(strip=True)) if views else None,
            "url": f"https://t.me/{post_id}", "source": f"scraped t.me/s/{channel}", "excluded": "",
        })
    return posts


def scrape_telegram():
    posts = []
    for entity, channel in config.TELEGRAM.items():
        found = parse_telegram(get(f"https://t.me/s/{channel}"), entity, channel)
        if not found:
            raise CollectError(f"Telegram {channel}: page loaded but no posts parsed")
        posts += found
    return posts


# ---------- X and LinkedIn imports ----------

def _require(path):
    try:
        return list(csv.DictReader(open(path, encoding="utf-8")))
    except FileNotFoundError:
        raise CollectError(f"Missing {path}. Put the X/LinkedIn export in the project folder.")


def import_x(path=config.X_CSV):
    posts = []
    for r in _require(path):
        excluded = "pinned" if is_true(r.get("is_pinned")) else "thread continuation" if is_true(r.get("is_continuation")) else ""
        posts.append({
            "entity": r["entity"], "channel": "X", "post_id": r["post_id"], "date": r.get("date") or None,
            "date_display": None, "text": r.get("text", ""), "format": r.get("format") or None,
            "likes": parse_count(r.get("likes")), "comments": parse_count(r.get("comments")),
            "reposts": parse_count(r.get("reposts")), "views": parse_count(r.get("views")),
            "url": r.get("source_url", ""), "source": "import (screenshot capture)", "excluded": excluded,
        })
    return posts


def import_linkedin(entity, path):
    posts = []
    for r in _require(path):
        excluded = ("pinned" if is_true(r.get("is_pinned")) else
                    "self-repost" if is_true(r.get("is_self_repost")) else
                    "continuation" if is_true(r.get("is_continuation")) else "")
        posts.append({
            "entity": entity, "channel": "LinkedIn", "post_id": r.get("record_id") or r.get("post_id"),
            "date": r.get("date") or None,  # screenshots only show "3w", "2mo" etc. Kept as display text, never converted.
            "date_display": r.get("date_display") or None,
            "text": r.get("visible_text_ocr") or r.get("text", ""), "format": r.get("format") or None,
            "likes": parse_count(r.get("likes")), "comments": parse_count(r.get("comments")),
            "reposts": parse_count(r.get("reposts")), "views": None,
            "url": r.get("source_url", ""), "source": "import (screenshot capture)", "excluded": excluded,
        })
    return posts


# ---------- Source library ----------

def clean_html(html):
    text = BeautifulSoup(html or "", "html.parser").get_text(" ", strip=True)
    return re.sub(r"\s+", " ", text)


def parse_rss(xml_text, limit=config.SOURCE_LIMIT):
    ns = {"content": "http://purl.org/rss/1.0/modules/content/"}
    items = ET.fromstring(xml_text).findall("./channel/item")[:limit]
    out = []
    for i, item in enumerate(items, 1):
        body = item.findtext("content:encoded", default="", namespaces=ns) or item.findtext("description", "")
        out.append({
            "id": f"S{i}", "type": "Re7 Research (Substack)", "title": item.findtext("title", "").strip(),
            "url": item.findtext("link", "").strip(), "date": item.findtext("pubDate", ""),
            "text": clean_html(body)[:6000],
        })
    return out


def parse_website(html, url, source_id):
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript", "svg"]):
        tag.decompose()
    title = soup.title.get_text(strip=True) if soup.title else url
    return {"id": source_id, "type": "Website", "title": title, "url": url, "date": "",
            "text": re.sub(r"\s+", " ", soup.get_text(" ", strip=True))[:6000]}


def fetch_sources():
    sources = parse_rss(get(config.RSS_URL))
    for url in config.WEBSITES:
        sources.append(parse_website(get(url), url, f"S{len(sources) + 1}"))
    sources = [s for s in sources if s["url"] and len(s["text"]) > 200]
    if len(sources) < 3:
        raise CollectError("Fewer than 3 usable Re7 sources fetched; refusing to draft without real material")
    return sources


def collect():
    posts = scrape_telegram() + import_x()
    for entity, path in config.LINKEDIN_CSVS.items():
        posts += import_linkedin(entity, path)
    return posts, fetch_sources()


def coverage(posts):
    rows = {}
    for p in posts:
        key = (p["entity"], p["channel"])
        r = rows.setdefault(key, {"entity": key[0], "channel": key[1], "captured": 0, "with_metric": 0,
                                  "source": p["source"]})
        r["captured"] += 1
        if p[config.METRIC[p["channel"]]] is not None:
            r["with_metric"] += 1
    for entity in ("Capital", "Labs"):
        for channel in ("X", "LinkedIn", "Telegram"):
            rows.setdefault((entity, channel), {"entity": entity, "channel": channel, "captured": 0,
                                                "with_metric": 0, "source": "no public channel found"})
    return sorted(rows.values(), key=lambda r: (r["entity"], r["channel"]))


def now_utc():
    return datetime.now(timezone.utc)
