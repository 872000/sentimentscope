"""Dashboard PNGs for SentimentScope (matplotlib, Agg backend — no display needed)."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

from .alerts import detect, load_config
from .data import DEFAULT_CONFIG_PATH, aggregate_daily, load_posts

ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"

COLORS = {
    "volume": "#5b8def",
    "sentiment": "#e07a2f",
    "alert_drop": "#d62728",
    "alert_surge": "#9467bd",
    "zero": "#888888",
}


def _slug(brand: str) -> str:
    return brand.lower().replace(" ", "-")


def brand_chart(rows: list[dict], alerts: list[dict], out: Path,
                figsize=(12, 5), dpi=150) -> Path:
    """Dual-axis chart: daily volume (bars) vs average sentiment (line)."""
    dates = [datetime.strptime(r["date"], "%Y-%m-%d") for r in rows]
    volumes = [r["volume"] for r in rows]
    scores = [r["avg_score"] for r in rows]
    brand = rows[0]["brand"]
    alert_dates = {a["date"] for a in alerts if a["brand"] == brand}

    fig, ax1 = plt.subplots(figsize=figsize, dpi=dpi)
    ax1.set_title(f"{brand} — volume vs sentiment", fontsize=14, pad=12)

    bars = ax1.bar(dates, volumes, width=0.7, color=COLORS["volume"],
                   alpha=0.75, label="Volume (posts)")
    for alert_date in alert_dates:
        idx = next(i for i, r in enumerate(rows) if r["date"] == alert_date)
        bars[idx].set_color(COLORS["alert_drop"])
        bars[idx].set_alpha(1.0)
    ax1.set_ylabel("Posts per day", color=COLORS["volume"])
    ax1.tick_params(axis="y", labelcolor=COLORS["volume"])
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))

    ax2 = ax1.twinx()
    ax2.plot(dates, scores, color=COLORS["sentiment"], marker="o",
             linewidth=2.5, label="Avg sentiment")
    ax2.axhline(0, color=COLORS["zero"], linestyle="--", linewidth=1)
    ax2.set_ylim(-1.05, 1.05)
    ax2.set_ylabel("Avg sentiment (-1 … +1)", color=COLORS["sentiment"])
    ax2.tick_params(axis="y", labelcolor=COLORS["sentiment"])
    for d in dates:
        if d.strftime("%Y-%m-%d") in alert_dates:
            ax2.annotate("ALERT", xy=(d, -0.95), ha="center", fontsize=8,
                         color="white",
                         bbox=dict(boxstyle="round,pad=0.3", fc=COLORS["alert_drop"], ec="none"))

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left",
               fontsize=9, framealpha=0.9)
    fig.tight_layout()
    fig.savefig(out)
    plt.close(fig)
    return out


def alert_timeline(alerts: list[dict], out: Path,
                   figsize=(12, 3.5), dpi=150) -> Path:
    """Timeline of all alerts: one row per brand, markers per alert.

    Alerts sharing a brand+date are fanned out vertically so every
    marker stays visible.
    """
    from collections import defaultdict
    from datetime import timedelta

    brands = sorted({a["brand"] for a in alerts})
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    ax.set_title("SentimentScope — alert timeline", fontsize=14, pad=12)

    ymap = {b: i for i, b in enumerate(brands)}
    groups: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for a in alerts:
        groups[(a["brand"], a["date"])].append(a)

    for (brand, date), group in sorted(groups.items()):
        d = datetime.strptime(date, "%Y-%m-%d")
        y = ymap[brand]
        for k, a in enumerate(group):
            offset = (k - (len(group) - 1) / 2) * 0.30
            color = (COLORS["alert_drop"] if a["type"] == "sentiment_drop"
                     else COLORS["alert_surge"])
            size = 220 if a["severity"] == "high" else 120
            ax.scatter([d], [y + offset], s=size, color=color,
                       alpha=0.85, edgecolors="black", linewidths=0.8, zorder=3)
            above = offset >= 0
            ax.annotate(f"{a['type']}\n({a['severity']})",
                        xy=(d, y + offset),
                        xytext=(0, 20 if above else -20),
                        textcoords="offset points",
                        ha="center", va="bottom" if above else "top", fontsize=8,
                        bbox=dict(boxstyle="round,pad=0.25", fc="white", ec=color))

    all_dates = [datetime.strptime(a["date"], "%Y-%m-%d") for a in alerts]
    pad = timedelta(days=1.2)
    ax.set_xlim(min(all_dates) - pad, max(all_dates) + pad)
    ax.xaxis.set_major_locator(mdates.DayLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))

    ax.set_yticks(list(ymap.values()))
    ax.set_yticklabels(brands)
    ax.tick_params(axis="y", length=0)
    ax.set_ylim(-0.9, len(brands) - 0.1)
    ax.grid(axis="x", alpha=0.3)
    for spine in ("top", "right", "left"):
        ax.spines[spine].set_visible(False)

    from matplotlib.lines import Line2D
    legend = [
        Line2D([0], [0], marker="o", color="w", markerfacecolor=COLORS["alert_drop"],
               markersize=10, label="sentiment_drop"),
        Line2D([0], [0], marker="o", color="w", markerfacecolor=COLORS["alert_surge"],
               markersize=10, label="negative_surge"),
    ]
    ax.legend(handles=legend, loc="upper right", fontsize=9)
    fig.tight_layout()
    fig.savefig(out)
    plt.close(fig)
    return out


def build(out_dir: str | Path = ASSETS_DIR,
          data_path=None, config_path: str = DEFAULT_CONFIG_PATH) -> dict:
    """Generate every dashboard PNG. Returns {name: path}."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    cfg = load_config(config_path) if isinstance(config_path, str) else config_path
    dash_cfg = json.load(open(DEFAULT_CONFIG_PATH))["dashboard"]

    posts = load_posts(data_path) if data_path else load_posts()
    daily = aggregate_daily(posts)
    alerts = detect(daily, cfg)

    made: dict[str, Path] = {}
    brands = sorted({r["brand"] for r in daily})
    for brand in brands:
        rows = [r for r in daily if r["brand"] == brand]
        path = out_dir / f"dashboard_{_slug(brand)}.png"
        brand_chart(rows, alerts, path,
                    figsize=tuple(dash_cfg["figsize"]), dpi=dash_cfg["dpi"])
        made[f"dashboard_{_slug(brand)}"] = path

    tl_path = out_dir / "alert_timeline.png"
    if alerts:
        alert_timeline(alerts, tl_path,
                       figsize=(12, max(3.5, 1.6 * len(brands))), dpi=dash_cfg["dpi"])
    else:
        fig, ax = plt.subplots(figsize=(12, 3), dpi=dash_cfg["dpi"])
        ax.text(0.5, 0.5, "No alerts — all brands stable.", ha="center",
                va="center", fontsize=13)
        ax.axis("off")
        fig.savefig(tl_path)
        plt.close(fig)
    made["alert_timeline"] = tl_path
    return made
