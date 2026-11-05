"""Settings for the Re7 social automation. Everything a reviewer might want to change lives here."""

MODEL = "claude-sonnet-5-5"

TELEGRAM = {"Labs": "re7labsalpha"}  # No verified public Re7 Capital channel was found, so Capital has no Telegram row.

X_CSV = "combined-x-screenshots.csv"
LINKEDIN_CSVS = {"Capital": "capital-linkedin-review.csv", "Labs": "labs-linkedin-review.csv"}

RSS_URL = "https://re7research.substack.com/feed"
WEBSITES = ["https://re7labs.xyz/"]
SOURCE_LIMIT = 5

# The metric each channel is ranked on. Views are reach, reactions are engagement. They are never mixed.
METRIC = {"X": "views", "LinkedIn": "likes", "Telegram": "views"}
METRIC_LABEL = {"X": "views", "LinkedIn": "reactions", "Telegram": "views"}

MIN_AGE_HOURS = 48
MIN_GROUP = 3

THEMES = [
    "Weekly promotion",          # "The Weekly is out" style posts
    "Research insight",          # a specific finding, report or chart from Re7 research
    "Market commentary",         # macro / market views, chart of the week
    "Media & events",            # podcasts, TV, interviews, conferences, panels
    "Product & vault update",    # Labs vaults, integrations, launches, grants
    "Risk & incident update",    # incident responses, risk notices
    "Company news",              # hiring, profiles, firm milestones
    "Education & explainer",     # how something works
]

FORMATS = ["text-only", "image", "chart/data visual", "video", "link post", "thread"]

BANNED = ["guaranteed", "guarantee", "risk-free", "risk free", "moon", "to the moon", "100x", "alpha leak",
          "passionate", "robust", "seamless", "transformative", "game-changer", "revolutionary",
          "dive into", "deep dive", "landscape"]

LIMITS = {"X": 280, "LinkedIn": 1300, "Telegram": 1000}
X_URL_LENGTH = 23  # X counts every link as 23 characters
