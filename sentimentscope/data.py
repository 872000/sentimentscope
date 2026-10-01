"""Loading and aggregating social posts for SentimentScope."""

from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

from .engine import analyze

PACKAGE_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DATA_PATH = PACKAGE_ROOT / "data" / "sample_posts.csv"
DEFAULT_CONFIG_PATH = PACKAGE_ROOT / "config.json"


def load_posts(path: str | Path = DEFAULT_DATA_PATH) -> list[dict]:
    """Load posts from CSV. Returns list of {id, brand, date, source, text}."""
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def score_posts(posts: list[dict]) -> list[dict]:
    """Attach ``score``/``label`` to every post (pure offline scoring)."""
    scored = []
    for post in posts:
        result = analyze(post["text"])
        scored.append({**post, "score": result["score"], "label": result["label"]})
    return scored


def aggregate_daily(posts: list[dict]) -> list[dict]:
    """Aggregate scored posts to one row per (brand, date).

    Row: {brand, date, volume, avg_score, pos, neu, neg, neg_share}.
    """
    scored = posts if posts and "score" in posts[0] else score_posts(posts)
    buckets: dict[tuple[str, str], list[float]] = defaultdict(list)
    labels: dict[tuple[str, str], list[str]] = defaultdict(list)
    for post in scored:
        key = (post["brand"], post["date"])
        buckets[key].append(post["score"])
        labels[key].append(post["label"])

    rows = []
    for (brand, date), scores in sorted(buckets.items()):
        lab = labels[(brand, date)]
        n = len(scores)
        neg = sum(1 for x in lab if x == "negative")
        rows.append({
            "brand": brand,
            "date": date,
            "volume": n,
            "avg_score": round(sum(scores) / n, 4),
            "pos": sum(1 for x in lab if x == "positive"),
            "neu": sum(1 for x in lab if x == "neutral"),
            "neg": neg,
            "neg_share": round(neg / n, 4),
        })
    return rows
