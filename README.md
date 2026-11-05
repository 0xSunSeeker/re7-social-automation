# Re7 social automation

One command collects Re7 Capital and Re7 Labs posts from X, LinkedIn and Telegram, has Claude label them by theme and format, ranks what performs best on each channel, and has Claude write nine new posts from Re7's own research.

```
pip install -r requirements.txt
echo 'ANTHROPIC_API_KEY=sk-ant-...' > .env
python run.py
```

Each run creates `runs/<timestamp>/` with `posts.csv`, `re7.sqlite`, `performance.csv`, `sources.json`, `drafts.json`, `report.md`, `report.pdf`, and `ai/` holding every API request and response. The latest `report.pdf` is also copied to the project root.

| File | Job |
|---|---|
| `collect.py` | Telegram scrape (t.me/s), X and LinkedIn CSV import, Re7 Research RSS and website |
| `analyse.py` | Claude theme labels, percentile ranking within entity and channel, Claude findings |
| `create.py` | Claude drafts plus checks on length, banned words, em dashes, links and numbers |
| `output.py` | CSV, SQLite, Markdown and PDF |
| `config.py` | Model, themes, formats, limits, banned words |

There is no sample data and no fallback copy. A missing key, missing CSV, failed fetch or a model answer that fails its checks twice stops the run.

X and LinkedIn come in as CSV because there is no API access to Re7's accounts. The included CSVs were built from screenshots of each feed. LinkedIn screenshots only show relative dates, so those are kept as shown.

`python -m pytest -q` runs offline tests against saved copies of the real Telegram page and RSS feed.
