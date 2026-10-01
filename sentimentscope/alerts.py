"""Spike detection: configurable alerts over daily brand aggregates.

Two alert types (see README for the rationale):

1. ``sentiment_drop`` — average sentiment fell by at least
   ``sentiment_drop_threshold`` vs the previous day (default 0.35),
   with enough volume to trust it (``min_volume``, default 20).
2. ``negative_surge`` — the share of negative posts jumped by at least
   ``negative_surge_threshold`` (default +0.25) vs the trailing 3-day
   mean, again with ``min_volume`` posts that day.

Severity: ``high`` when the move is 1.4x the threshold, else ``medium``.
"""

from __future__ import annotations

import json
from statistics import mean

from .data import DEFAULT_CONFIG_PATH


def load_config(path: str = DEFAULT_CONFIG_PATH) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)["alerts"]


def _severity(move: float, threshold: float) -> str:
    return "high" if abs(move) >= 1.4 * threshold else "medium"


def detect(daily: list[dict], config: dict | None = None) -> list[dict]:
    """Scan daily aggregates (from :func:`aggregate_daily`) for spikes."""
    cfg = config or load_config()
    drop_t = cfg.get("sentiment_drop_threshold", 0.35)
    surge_t = cfg.get("negative_surge_threshold", 0.25)
    min_vol = cfg.get("min_volume", 20)

    by_brand: dict[str, list[dict]] = {}
    for row in daily:
        by_brand.setdefault(row["brand"], []).append(row)
    for rows in by_brand.values():
        rows.sort(key=lambda r: r["date"])

    alerts: list[dict] = []
    for brand, rows in by_brand.items():
        for i, row in enumerate(rows):
            if row["volume"] < min_vol:
                continue

            # 1) sharp day-over-day sentiment drop
            if i > 0:
                prev = rows[i - 1]
                move = row["avg_score"] - prev["avg_score"]
                if move <= -drop_t:
                    alerts.append({
                        "brand": brand,
                        "date": row["date"],
                        "type": "sentiment_drop",
                        "severity": _severity(move, drop_t),
                        "message": (
                            f"{brand}: sentiment dropped {move:+.2f} "
                            f"({prev['avg_score']:+.2f} -> {row['avg_score']:+.2f}) "
                            f"on {row['date']} across {row['volume']} posts."
                        ),
                        "metrics": {
                            "move": round(move, 4),
                            "prev_avg": prev["avg_score"],
                            "avg": row["avg_score"],
                            "volume": row["volume"],
                        },
                    })

            # 2) negative-volume surge vs trailing 3-day mean
            if i >= 2:
                baseline = mean(r["neg_share"] for r in rows[max(0, i - 3):i])
                move = row["neg_share"] - baseline
                if move >= surge_t:
                    alerts.append({
                        "brand": brand,
                        "date": row["date"],
                        "type": "negative_surge",
                        "severity": _severity(move, surge_t),
                        "message": (
                            f"{brand}: negative share surged {move:+.0%} "
                            f"({baseline:.0%} -> {row['neg_share']:.0%}) "
                            f"on {row['date']} ({row['neg']} of {row['volume']} posts)."
                        ),
                        "metrics": {
                            "move": round(move, 4),
                            "baseline_neg_share": round(baseline, 4),
                            "neg_share": row["neg_share"],
                            "volume": row["volume"],
                        },
                    })

    alerts.sort(key=lambda a: (a["date"], a["brand"], a["type"]))
    return alerts
