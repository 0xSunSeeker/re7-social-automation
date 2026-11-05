"""Tests run offline. The fake client below exists only here; run.py always uses the real Anthropic API."""
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
FIX = ROOT / "tests" / "fixtures"
sys.path.insert(0, str(ROOT))
os.chdir(ROOT)

import ai, analyse, collect, config, create  # noqa: E402


def test_parse_count_keeps_missing_as_none():
    assert collect.parse_count("1.2K") == 1200
    assert collect.parse_count("2M") == 2_000_000
    assert collect.parse_count("0") == 0
    assert collect.parse_count("") is None and collect.parse_count(None) is None


def test_telegram_parser_on_real_snapshot():
    posts = collect.parse_telegram((FIX / "telegram.html").read_text(), "Labs", "re7labsalpha")
    assert len(posts) == 20
    assert all(p["views"] is not None and p["likes"] is None for p in posts)
    assert {p["format"] for p in posts} <= set(config.FORMATS)


def test_rss_parser_on_real_snapshot():
    sources = collect.parse_rss((FIX / "research.xml").read_text())
    assert len(sources) == 5
    assert all(s["url"].startswith("https://") and len(s["text"]) > 200 for s in sources)


def test_imports_flag_exclusions_and_never_invent_dates():
    x = collect.import_x()
    assert any(p["excluded"] == "pinned" for p in x)
    li = collect.import_linkedin("Capital", config.LINKEDIN_CSVS["Capital"])
    assert all(p["date"] is None and p["date_display"] for p in li)
    assert all(p["views"] is None for p in li)


def test_missing_csv_stops_the_run():
    with pytest.raises(collect.CollectError):
        collect.import_x("does-not-exist.csv")


def test_scoring_is_within_entity_and_channel_and_handles_ties():
    now = datetime(2026, 11, 5, tzinfo=timezone.utc)
    def post(entity, channel, views, excluded=""):
        return {"entity": entity, "channel": channel, "views": views, "likes": None, "date": "2026-10-01T00:00:00+00:00", "excluded": excluded}
    posts = [post("Labs", "X", 100), post("Labs", "X", 200), post("Labs", "X", 200), post("Capital", "X", 5),
             post("Labs", "X", 9999, excluded="pinned"), post("Labs", "X", None)]
    analyse.score(posts, now)
    assert [p["percentile"] for p in posts[:3]] == [0.0, 75.0, 75.0]
    assert posts[3]["percentile"] is None  # alone in its cohort
    assert posts[4]["excluded"] == "pinned" and posts[5]["excluded"] == "no metric"


SRC = {"S1": {"id": "S1", "title": "The Weekly", "url": "https://re7research.substack.com/p/x",
              "text": "Exposure splits into chain, protocol and asset layers. 99% of hacks were not AI."}}


def test_draft_checks():
    ok = {"channel": "X", "source_id": "S1", "text": "Risk has three layers: chain, protocol and asset."}
    assert create.validate(ok, SRC) == []
    assert create.validate({**ok, "text": "Guaranteed 12% yield"}, SRC)       # banned word + invented number
    assert create.validate({**ok, "text": "Three layers — chain"}, SRC)  # em dash
    assert create.validate({**ok, "text": "x" * 260}, SRC)                     # too long once the link is added
    assert create.validate({**ok, "text": "99% of hacks were not AI."}, SRC) == []
    assert create.validate({**ok, "source_id": "S9"}, SRC)


def test_numbers_must_be_grounded():
    assert ai.unsupported_numbers("3.3K views, median 1,100", {3300, 1100}) == []
    assert ai.unsupported_numbers("up 2.4x", {3300}) == [2.4]


def test_no_api_key_stops_the_run(tmp_path, monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    with pytest.raises(ai.AIError):
        ai.setup(tmp_path)
