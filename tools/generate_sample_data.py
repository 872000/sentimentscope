"""Generate the bundled sample dataset (seeded, reproducible, fully fictional).

Three fictional brands over 7 days (2026-09-21 .. 2026-09-27):

- VoltBean Coffee   — steadily positive baseline.
- Nimbus Airlines   — mixed baseline, then a scripted PR incident on
                      2026-09-25: a wave of flight cancellations that
                      floods the feed with angry posts and tanks sentiment.
                      This is the demo target for the spike detector.
- PixelNest Games   — neutral-to-mildly-positive baseline.

Run:  python3 tools/generate_sample_data.py
Writes: data/sample_posts.csv  (id, brand, date, source, text)
"""

import csv
import random
from pathlib import Path

SEED = 20260925
OUT = Path(__file__).resolve().parent.parent / "data" / "sample_posts.csv"

DAYS = [f"2026-09-{d:02d}" for d in range(21, 28)]
SOURCES = ["twitter", "reddit", "instagram", "threads"]

BRAND_CONTEXT = {
    "VoltBean Coffee": ["oat latte", "cold brew", "espresso", "barista",
                        "croissant", "morning rush", "loyalty app"],
    "Nimbus Airlines": ["flight", "boarding", "gate agent", "legroom",
                        "baggage claim", "pilot", "check-in"],
    "PixelNest Games": ["new update", "servers", "quest line", "graphics",
                        "patch notes", "matchmaking", "season pass"],
}

POSITIVE_TEMPLATES = [
    "Love the {item} at {brand} — absolutely fantastic!",
    "{brand} never disappoints, the {item} was superb today.",
    "Really impressed with {brand}'s {item}. Highly recommend!",
    "The {item} from {brand} was wonderful. Great experience overall.",
    "{brand} has the friendliest staff and the {item} is always perfect.",
    "Delighted with {brand} today — smooth, quick, and genuinely excellent.",
    "Shoutout to {brand}: the {item} was amazing and the service was lovely.",
    "{brand}'s {item} keeps getting better. Truly outstanding!",
    "Had a great time with {brand}'s {item}. Clean, fast, and delightful.",
    "The {item} at {brand} was delicious and the whole vibe was cozy.",
    "Very happy with {brand} — reliable {item} and super helpful team.",
    "{brand} is easily the best in town for {item}. Phenomenal!",
]

NEGATIVE_TEMPLATES = [
    "Waited forever for my {item} at {brand}. Terrible service.",
    "{brand} was a complete disaster today. Never again.",
    "Really disappointed with {brand}'s {item} — sloppy and overpriced.",
    "The {item} at {brand} was awful. Rude staff, total mess.",
    "{brand} keeps getting worse. The {item} was mediocre at best.",
    "Frustrating experience with {brand}'s {item}. Broken promises.",
    "Not impressed with {brand} at all. The {item} was bland and slow.",
    "Ugh, {brand}'s {item} was a letdown. Definitely not worth it.",
    "{brand} charged me extra for a terrible {item}. Feels like a ripoff.",
    "Avoid {brand}'s {item} — confusing, slow, and really poor quality.",
]

NEUTRAL_TEMPLATES = [
    "Tried {brand}'s {item} yesterday. Nothing special, nothing bad.",
    "The {item} at {brand} was fine. About what I expected.",
    "Used {brand} for the {item} again. It works, I guess.",
    "Meh. {brand}'s {item} is okay but not worth the hype.",
    "The {item} from {brand} was decent. Might go back, might not.",
    "No strong feelings about {brand}'s {item}. It was average.",
]

# --- The scripted PR incident: Nimbus Airlines, 2026-09-25 ---------------
INCIDENT_DATE = "2026-09-25"
INCIDENT_TEMPLATES = [
    "Flight NB-482 cancelled with zero warning, stranded at the gate. Appalling!",
    "Nimbus just cancelled our flight and offered NO refund. Outrageous scam.",
    "Stuck overnight because Nimbus cancelled everything. Worst airline experience ever.",
    "Missed my sister's wedding thanks to Nimbus. Furious doesn't cover it.",
    "Gate agent was rude and dismissive when our flight was cancelled. Disgraceful.",
    "Third cancellation this week from Nimbus. Completely unreliable.",
    "Nimbus left 200 of us stranded with no hotel, no food, no answers. Nightmare.",
    "They bumped us off the flight then cancelled the rebooking. Absolute chaos.",
    "Nimbus cancelled my connecting flight and the helpline hung up on me. Pathetic.",
    "Slept on the terminal floor because Nimbus cancelled the last flight out. Miserable.",
    "Nimbus ruined our anniversary trip with a last-minute cancellation. Heartbreaking.",
    "Cancelled flight, lost baggage, zero communication. Nimbus is a catastrophe.",
    "Never flying Nimbus again. Stranded, ignored, and overcharged. Atrocious.",
    "The Nimbus cancellation meltdown continues — day two of chaos at the terminal.",
]


def build_posts() -> list[dict]:
    rng = random.Random(SEED)
    posts: list[dict] = []
    pid = 1

    def add(brand: str, date: str, text: str):
        nonlocal pid
        posts.append({
            "id": pid,
            "brand": brand,
            "date": date,
            "source": rng.choice(SOURCES),
            "text": text,
        })
        pid += 1

    for brand in BRAND_CONTEXT:
        for date in DAYS:
            ctx = BRAND_CONTEXT[brand]
            item = lambda: rng.choice(ctx)  # noqa: E731

            if brand == "Nimbus Airlines" and date == INCIDENT_DATE:
                # PR incident: high volume, overwhelmingly negative
                n = 90
                neg_pool = INCIDENT_TEMPLATES + NEGATIVE_TEMPLATES
                for _ in range(n):
                    r = rng.random()
                    if r < 0.78:
                        t = rng.choice(INCIDENT_TEMPLATES)
                    elif r < 0.88:
                        t = rng.choice(NEGATIVE_TEMPLATES).format(
                            brand=brand, item=item())
                    else:
                        t = rng.choice(NEUTRAL_TEMPLATES).format(
                            brand=brand, item=item())
                    add(brand, date, t)
                continue

            if brand == "Nimbus Airlines" and date in ("2026-09-26", "2026-09-27"):
                # aftershock: elevated negativity, apologising staff mentions
                n = rng.randint(38, 48)
                mix = [0.45, 0.30, 0.25]
            elif brand == "VoltBean Coffee":
                n = rng.randint(28, 40)
                mix = [0.62, 0.18, 0.20]   # pos, neg, neu
            elif brand == "PixelNest Games":
                n = rng.randint(22, 34)
                mix = [0.40, 0.22, 0.38]
            else:  # Nimbus baseline: mixed
                n = rng.randint(25, 36)
                mix = [0.42, 0.32, 0.26]

            for _ in range(n):
                r = rng.random()
                if r < mix[0]:
                    t = rng.choice(POSITIVE_TEMPLATES).format(
                        brand=brand, item=item())
                elif r < mix[0] + mix[1]:
                    t = rng.choice(NEGATIVE_TEMPLATES).format(
                        brand=brand, item=item())
                else:
                    t = rng.choice(NEUTRAL_TEMPLATES).format(
                        brand=brand, item=item())
                add(brand, date, t)

    return posts


def main():
    posts = build_posts()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "brand", "date", "source", "text"])
        writer.writeheader()
        writer.writerows(posts)
    # quick summary
    from collections import Counter
    print(f"Wrote {len(posts)} posts -> {OUT}")
    print(Counter((p["brand"], p["date"]) for p in posts))


if __name__ == "__main__":
    main()
