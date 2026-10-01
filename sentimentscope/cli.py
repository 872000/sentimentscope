"""SentimentScope CLI.

Commands:
    analyze    score text(s) or posts from the bundled dataset
    dashboard  generate PNG dashboards + print a text summary
    alerts     run spike detection and print alerts
    demo       end-to-end demo: score -> aggregate -> alerts -> dashboard
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .alerts import detect, load_config
from .dashboard import build as build_dashboard
from .data import DEFAULT_DATA_PATH, aggregate_daily, load_posts, score_posts
from .engine import analyze


def cmd_analyze(args) -> int:
    texts: list[str] = []
    if args.text:
        texts = [" ".join(args.text)]
    elif args.dataset:
        posts = load_posts(args.dataset)
        if args.brand:
            posts = [p for p in posts if p["brand"] == args.brand]
        if args.date:
            posts = [p for p in posts if p["date"] == args.date]
        posts = posts[: args.limit]
        if not posts:
            print("No posts matched the filters.", file=sys.stderr)
            return 1
        scored = score_posts(posts)
        print(f"{'score':>7}  {'label':8}  text")
        print("-" * 70)
        for p in scored:
            text = p["text"][:58] + ("…" if len(p["text"]) > 58 else "")
            print(f"{p['score']:>+7.3f}  {p['label']:8}  {text}")
        return 0
    else:
        print("Give TEXT to score, or --dataset to score bundled posts.",
              file=sys.stderr)
        return 2

    for text in texts:
        r = analyze(text)
        print(f"score: {r['score']:+.4f}   label: {r['label']}")
        if args.verbose:
            for token, contrib in r["tokens"]:
                print(f"    {token!r:20} {contrib:+.3f}")
    return 0


def _summarise(daily: list[dict], alerts: list[dict]) -> str:
    lines = ["Brand sentiment summary", "=" * 60]
    for brand in sorted({r["brand"] for r in daily}):
        rows = [r for r in daily if r["brand"] == brand]
        avg = sum(r["avg_score"] for r in rows) / len(rows)
        vol = sum(r["volume"] for r in rows)
        n_alerts = sum(1 for a in alerts if a["brand"] == brand)
        lines.append(
            f"{brand:18} avg {avg:+.3f} | {vol:4d} posts | {n_alerts} alert(s)")
    lines.append("=" * 60)
    lines.append(f"Total alerts: {len(alerts)}")
    return "\n".join(lines)


def cmd_dashboard(args) -> int:
    posts = load_posts(args.dataset)
    daily = aggregate_daily(posts)
    alerts = detect(daily, load_config(args.config))
    made = build_dashboard(out_dir=args.out, data_path=args.dataset,
                           config_path=args.config)
    print(_summarise(daily, alerts))
    print()
    for name, path in made.items():
        print(f"  wrote {name}: {path}")
    return 0


def cmd_alerts(args) -> int:
    daily = aggregate_daily(load_posts(args.dataset))
    alerts = detect(daily, load_config(args.config))
    if args.json:
        print(json.dumps(alerts, indent=2))
    elif not alerts:
        print("No alerts — all brands stable.")
    else:
        for a in alerts:
            print(f"[{a['severity'].upper():6}] {a['type']:15} "
                  f"{a['brand']} on {a['date']}")
            print(f"          {a['message']}")
    return 0


def cmd_demo(args) -> int:
    print("SentimentScope demo — end to end")
    print("=" * 60)
    print("\n1) Scoring engine on tricky inputs:")
    for t in ["not good", "very good", "The coffee was served at noon",
              "TERRIBLE service!!", "not bad at all"]:
        r = analyze(t)
        print(f"   {t!r:38} -> {r['score']:+.3f} ({r['label']})")
    print("\n2) Aggregating bundled posts (3 fictional brands, 7 days)…")
    daily = aggregate_daily(load_posts(args.dataset))
    print(f"   {len(daily)} brand-day rows from {sum(r['volume'] for r in daily)} posts")
    print("\n3) Spike detection:")
    alerts = detect(daily, load_config(args.config))
    for a in alerts:
        print(f"   [{a['severity'].upper()}] {a['message']}")
    print("\n4) Generating dashboards…")
    made = build_dashboard(out_dir=args.out, data_path=args.dataset,
                           config_path=args.config)
    for name, path in made.items():
        print(f"   wrote {path}")
    print("\n" + _summarise(daily, alerts))
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="sentimentscope",
        description="Brand sentiment radar — lexicon-based, fully offline.")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("analyze", help="Score text or dataset posts.")
    p.add_argument("text", nargs="*", help="Text to score.")
    p.add_argument("--dataset", default=str(DEFAULT_DATA_PATH),
                   help="CSV of posts to score instead of TEXT.")
    p.add_argument("--brand", help="Filter dataset by brand.")
    p.add_argument("--date", help="Filter dataset by date (YYYY-MM-DD).")
    p.add_argument("--limit", type=int, default=10, help="Max posts to show.")
    p.add_argument("-v", "--verbose", action="store_true",
                   help="Show per-token contributions.")
    p.set_defaults(func=cmd_analyze)

    p = sub.add_parser("dashboard", help="Generate PNG dashboards + summary.")
    p.add_argument("--dataset", default=str(DEFAULT_DATA_PATH))
    p.add_argument("--config", default="config.json")
    p.add_argument("--out", default="assets", help="Output directory for PNGs.")
    p.set_defaults(func=cmd_dashboard)

    p = sub.add_parser("alerts", help="Run spike detection.")
    p.add_argument("--dataset", default=str(DEFAULT_DATA_PATH))
    p.add_argument("--config", default="config.json")
    p.add_argument("--json", action="store_true", help="Machine-readable output.")
    p.set_defaults(func=cmd_alerts)

    p = sub.add_parser("demo", help="End-to-end demo.")
    p.add_argument("--dataset", default=str(DEFAULT_DATA_PATH))
    p.add_argument("--config", default="config.json")
    p.add_argument("--out", default="assets")
    p.set_defaults(func=cmd_demo)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
