"""Hand-built sentiment lexicon for SentimentScope.

Every entry was curated by hand — no pretrained models, no API calls.
Each word carries a *base weight*:

- ``1.0`` — standard sentiment word  (e.g. "good", "bad")
- ``2.0`` — strong sentiment word    (e.g. "phenomenal", "atrocious")

The scoring engine in :mod:`sentimentscope.engine` adjusts these base
weights with negation ("not good"), intensifiers ("very"), caps and
punctuation before normalising to ``[-1, +1]``.

Entries: ~230 positive, ~235 negative.
"""

# word -> base weight
POSITIVE = {
    # --- strong (2.0) ---
    "phenomenal": 2.0, "outstanding": 2.0, "superb": 2.0, "exceptional": 2.0,
    "magnificent": 2.0, "fantastic": 2.0, "incredible": 2.0, "amazing": 2.0,
    "wonderful": 2.0, "brilliant": 2.0, "perfect": 2.0, "flawless": 2.0,
    "masterful": 2.0, "exemplary": 2.0, "stellar": 2.0, "legendary": 2.0,
    "breathtaking": 2.0, "spectacular": 2.0, "astonishing": 2.0,
    "unforgettable": 2.0, "topnotch": 2.0, "top-notch": 2.0,
    "first-rate": 2.0, "first-class": 2.0, "world-class": 2.0,
    "impeccable": 2.0, "supreme": 2.0, "sublime": 2.0,
    # --- standard (1.0) ---
    "good": 1.0, "great": 1.0, "nice": 1.0, "fine": 1.0, "decent": 1.0,
    "solid": 1.0, "reliable": 1.0, "dependable": 1.0, "trustworthy": 1.0,
    "pleasant": 1.0, "enjoyable": 1.0, "lovely": 1.0, "delightful": 1.0,
    "charming": 1.0, "cheerful": 1.0, "happy": 1.0, "glad": 1.0,
    "thrilled": 1.0, "excited": 1.0, "delighted": 1.0, "impressed": 1.0,
    "satisfied": 1.0, "pleased": 1.0, "content": 1.0, "grateful": 1.0,
    "thankful": 1.0, "appreciate": 1.0, "love": 1.0, "loved": 1.0,
    "loving": 1.0, "like": 1.0, "liked": 1.0, "adore": 1.0, "admire": 1.0,
    "recommend": 1.0, "recommended": 1.0, "favourite": 1.0, "favorite": 1.0,
    "best": 1.0, "better": 1.0, "excellent": 1.0, "superior": 1.0,
    "premium": 1.0, "quality": 1.0, "awesome": 1.0, "cool": 1.0,
    "smooth": 1.0, "seamless": 1.0, "effortless": 1.0, "easy": 1.0,
    "convenient": 1.0, "fast": 1.0, "quick": 1.0, "prompt": 1.0,
    "efficient": 1.0, "responsive": 1.0, "helpful": 1.0, "friendly": 1.0,
    "courteous": 1.0, "polite": 1.0, "professional": 1.0, "skilled": 1.0,
    "talented": 1.0, "knowledgeable": 1.0, "honest": 1.0, "fair": 1.0,
    "reasonable": 1.0, "affordable": 1.0, "worth": 1.0, "valuable": 1.0,
    "clean": 1.0, "fresh": 1.0, "crisp": 1.0, "bright": 1.0, "warm": 1.0,
    "cozy": 1.0, "comfortable": 1.0, "relaxing": 1.0, "calm": 1.0,
    "peaceful": 1.0, "beautiful": 1.0, "gorgeous": 1.0, "pretty": 1.0,
    "stunning": 1.0, "elegant": 1.0, "stylish": 1.0, "sleek": 1.0,
    "modern": 1.0, "innovative": 1.0, "creative": 1.0, "clever": 1.0,
    "smart": 1.0, "genius": 1.0, "fun": 1.0, "funny": 1.0, "hilarious": 1.0,
    "entertaining": 1.0, "engaging": 1.0, "captivating": 1.0,
    "delicious": 1.0, "tasty": 1.0, "yummy": 1.0, "flavorful": 1.0,
    "refreshing": 1.0, "smoothly": 1.0, "win": 1.0, "winner": 1.0,
    "winning": 1.0, "success": 1.0, "successful": 1.0, "triumph": 1.0,
    "victory": 1.0, "lucky": 1.0, "fortunate": 1.0, "blessed": 1.0,
    "proud": 1.0, "confident": 1.0, "safe": 1.0, "secure": 1.0,
    "protected": 1.0, "healthy": 1.0, "energetic": 1.0, "refreshed": 1.0,
    "restored": 1.0, "fixed": 1.0, "resolved": 1.0, "improved": 1.0,
    "improvement": 1.0, "upgrade": 1.0, "upgraded": 1.0, "bonus": 1.0,
    "free": 1.0, "discount": 1.0, "deal": 1.0, "steal": 1.0, "bargain": 1.0,
    "shine": 1.0, "shining": 1.0, "glow": 1.0, "sparkle": 1.0,
    "wow": 1.0, "yay": 1.0, "bravo": 1.0, "kudos": 1.0, "props": 1.0,
    "respect": 1.0, "trust": 1.0, "loyal": 1.0, "faithful": 1.0,
    "sweet": 1.0, "kind": 1.0, "generous": 1.0, "thoughtful": 1.0,
    "caring": 1.0, "sincere": 1.0, "authentic": 1.0, "genuine": 1.0,
    "real": 1.0, "pure": 1.0, "natural": 1.0, "organic": 1.0,
    "vibrant": 1.0, "lively": 1.0, "dynamic": 1.0, "powerful": 1.0,
    "strong": 1.0, "sturdy": 1.0, "durable": 1.0, "lasting": 1.0,
    "memorable": 1.0, "special": 1.0, "unique": 1.0, "rare": 1.0,
    "exciting": 1.0, "thrilling": 1.0, "inspiring": 1.0, "motivating": 1.0,
    "uplifting": 1.0, "heartwarming": 1.0, "touching": 1.0, "moving": 1.0,
    "graceful": 1.0, "poised": 1.0, "classy": 1.0, "fancy": 1.0,
    "luxurious": 1.0, "plush": 1.0, "spacious": 1.0, "airy": 1.0,
    "quiet": 1.0, "serene": 1.0, "tranquil": 1.0, "heavenly": 1.0,
    "divine": 1.0, "magical": 1.0, "enchanting": 1.0, "mesmerizing": 1.0,
    "impressive": 1.0, "remarkable": 1.0, "notable": 1.0, "praise": 1.0,
    "praised": 1.0, "compliment": 1.0, "acclaimed": 1.0, "celebrated": 1.0,
    "rewarding": 1.0, "fulfilling": 1.0, "satisfying": 1.0, "rich": 1.0,
    "bold": 1.0, "vivid": 1.0, "colorful": 1.0, "radiant": 1.0,
    "optimistic": 1.0, "hopeful": 1.0, "promising": 1.0, "encouraging": 1.0,
    "reassuring": 1.0, "comforting": 1.0, "soothing": 1.0, "healing": 1.0,
    "revitalizing": 1.0, "rejuvenating": 1.0, "exhilarating": 1.0,
    "electrifying": 1.0, "addictive": 1.0, "obsessed": 1.0,
}

NEGATIVE = {
    # --- strong (-2.0) ---
    "atrocious": -2.0, "horrendous": -2.0, "appalling": -2.0,
    "dreadful": -2.0, "abysmal": -2.0, "catastrophic": -2.0,
    "disastrous": -2.0, "horrible": -2.0, "hideous": -2.0,
    "nightmarish": -2.0, "outrageous": -2.0, "scandalous": -2.0,
    "disgraceful": -2.0, "shameful": -2.0, "deplorable": -2.0,
    "despicable": -2.0, "vile": -2.0, "repulsive": -2.0,
    "revolting": -2.0, "abhorrent": -2.0, "horrifying": -2.0,
    "terrifying": -2.0, "traumatizing": -2.0, "devastating": -2.0,
    "heartbreaking": -2.0, "unbearable": -2.0, "intolerable": -2.0,
    "unacceptable": -2.0, "unforgivable": -2.0, "inexcusable": -2.0,
    "worthless": -2.0, "useless": -2.0, "pathetic": -2.0,
    "miserable": -2.0, "wretched": -2.0, "pitiful": -2.0,
    # --- standard (-1.0) ---
    "bad": -1.0, "worse": -1.0, "worst": -1.0, "poor": -1.0,
    "terrible": -1.0, "awful": -1.0, "disappointing": -1.0,
    "disappointed": -1.0, "underwhelming": -1.0, "mediocre": -1.0,
    "subpar": -1.0, "lacking": -1.0, "weak": -1.0, "flimsy": -1.0,
    "cheap": -1.0, "tacky": -1.0, "ugly": -1.0, "unattractive": -1.0,
    "boring": -1.0, "dull": -1.0, "bland": -1.0, "tasteless": -1.0,
    "stale": -1.0, "stinky": -1.0, "smelly": -1.0, "gross": -1.0,
    "nasty": -1.0, "disgusting": -1.0, "filthy": -1.0, "dirty": -1.0,
    "messy": -1.0, "sloppy": -1.0, "careless": -1.0, "reckless": -1.0,
    "slow": -1.0, "sluggish": -1.0, "laggy": -1.0, "delayed": -1.0,
    "late": -1.0, "overdue": -1.0, "cancelled": -1.0, "canceled": -1.0,
    "broken": -1.0, "defective": -1.0, "faulty": -1.0, "buggy": -1.0,
    "glitchy": -1.0, "crashed": -1.0, "crashing": -1.0, "frozen": -1.0,
    "stuck": -1.0, "dead": -1.0, "killed": -1.0, "ruined": -1.0,
    "destroyed": -1.0, "wrecked": -1.0, "damaged": -1.0, "scratched": -1.0,
    "dented": -1.0, "leaking": -1.0, "leak": -1.0, "spilled": -1.0,
    "cold": -1.0, "lukewarm": -1.0, "burnt": -1.0, "burned": -1.0,
    "overcooked": -1.0, "undercooked": -1.0, "soggy": -1.0, "watery": -1.0,
    "bitter": -1.0, "sour": -1.0, "salty": -1.0, "greasy": -1.0,
    "oily": -1.0, "rubbery": -1.0, "chewy": -1.0, "tough": -1.0,
    "hate": -1.0, "hated": -1.0, "hateful": -1.0, "despise": -1.0,
    "loathe": -1.0, "detest": -1.0, "dislike": -1.0, "disliked": -1.0,
    "regret": -1.0, "regretted": -1.0, "sorry": -1.0, "apologize": -1.0,
    "apology": -1.0, "complaint": -1.0, "complain": -1.0, "complained": -1.0,
    "whine": -1.0, "rant": -1.0, "furious": -1.0, "angry": -1.0,
    "annoyed": -1.0, "annoying": -1.0, "irritated": -1.0, "irritating": -1.0,
    "frustrated": -1.0, "frustrating": -1.0, "infuriating": -1.0,
    "maddening": -1.0, "aggravating": -1.0, "upset": -1.0, "upsetting": -1.0,
    "sad": -1.0, "depressing": -1.0, "depressed": -1.0, "gloomy": -1.0,
    "bleak": -1.0, "grim": -1.0, "hopeless": -1.0, "despair": -1.0,
    "worried": -1.0, "worrying": -1.0, "anxious": -1.0, "nervous": -1.0,
    "scared": -1.0, "fearful": -1.0, "afraid": -1.0, "panic": -1.0,
    "panicked": -1.0, "stressed": -1.0, "stressful": -1.0, "tense": -1.0,
    "uncomfortable": -1.0, "painful": -1.0, "hurt": -1.0, "aching": -1.0,
    "sick": -1.0, "nauseating": -1.0, "dizzy": -1.0, "exhausted": -1.0,
    "tired": -1.0, "drained": -1.0, "overworked": -1.0, "burnout": -1.0,
    "rude": -1.0, "arrogant": -1.0, "condescending": -1.0, "dismissive": -1.0,
    "unhelpful": -1.0, "unfriendly": -1.0, "hostile": -1.0, "hostility": -1.0,
    "mean": -1.0, "cruel": -1.0, "harsh": -1.0, "abrasive": -1.0,
    "obnoxious": -1.0, "obnoxiously": -1.0, "ignorant": -1.0,
    "incompetent": -1.0, "clueless": -1.0, "uselessly": -1.0,
    "unprofessional": -1.0, "unethical": -1.0, "dishonest": -1.0,
    "deceptive": -1.0, "misleading": -1.0, "scam": -1.0, "scammed": -1.0,
    "ripoff": -1.0, "overpriced": -1.0, "expensive": -1.0, "pricey": -1.0,
    "waste": -1.0, "wasted": -1.0, "wasteful": -1.0, "overcharged": -1.0,
    "hidden": -1.0, "fee": -1.0, "fees": -1.0, "penalty": -1.0,
    "fine_print": -1.0, "trap": -1.0, "nightmare": -1.0, "fiasco": -1.0,
    "debacle": -1.0, "disaster": -1.0, "catastrophe": -1.0, "meltdown": -1.0,
    "chaos": -1.0, "chaotic": -1.0, "confusion": -1.0, "confusing": -1.0,
    "miscommunication": -1.0, "stranded": -1.0, "abandoned": -1.0,
    "neglected": -1.0, "ignored": -1.0, "dismissed": -1.0, "rejected": -1.0,
    "denied": -1.0, "refused": -1.0, "failed": -1.0, "failing": -1.0,
    "failure": -1.0, "flop": -1.0, "loser": -1.0, "losing": -1.0,
    "decline": -1.0, "declining": -1.0, "deteriorating": -1.0,
    "worrisome": -1.0, "alarming": -1.0, "shocking": -1.0, "shocked": -1.0,
    "embarrassing": -1.0, "humiliating": -1.0, "awkward": -1.0,
    "uncomfortable": -1.0, "pain": -1.0, "suffering": -1.0, "agony": -1.0,
    "dread": -1.0, "dreaded": -1.0, "regrettable": -1.0, "unfortunate": -1.0,
    "unlucky": -1.0, "cursed": -1.0, "jinxed": -1.0, "doomed": -1.0,
    "toxic": -1.0, "poisonous": -1.0, "harmful": -1.0, "dangerous": -1.0,
    "risky": -1.0, "unsafe": -1.0, "threat": -1.0, "threatening": -1.0,
}

#: Words that flip the sentiment of the tokens that follow them.
NEGATORS = {
    "not", "no", "never", "none", "nobody", "nothing", "nowhere", "neither",
    "nor", "scarcely", "without", "aint", "cannot",
    # Note: "hardly"/"barely" are handled as diminishers in INTENSIFIERS,
    # not as negators — "barely good" is weak praise, not its opposite.
}

# Contraction forms handled during tokenisation ("don't" -> "do n't")
NEGATION_CONTRACTIONS = {
    "don't": "not", "doesn't": "not", "didn't": "not", "isn't": "not",
    "aren't": "not", "wasn't": "not", "weren't": "not", "haven't": "not",
    "hasn't": "not", "hadn't": "not", "won't": "not", "wouldn't": "not",
    "can't": "not", "couldn't": "not", "shouldn't": "not", "mustn't": "not",
}

#: Intensifier word -> multiplier applied to the next sentiment token.
INTENSIFIERS = {
    "extremely": 2.0, "incredibly": 2.0, "exceptionally": 2.0,
    "absolutely": 2.0, "totally": 2.0, "completely": 2.0, "utterly": 2.0,
    "thoroughly": 2.0, "highly": 1.8, "deeply": 1.8, "truly": 1.6,
    "really": 1.5, "very": 1.5, "so": 1.5, "super": 1.6, "quite": 1.25,
    "pretty": 1.25, "rather": 1.25, "fairly": 1.15, "somewhat": 0.7,
    "slightly": 0.5, "little": 0.6, "marginally": 0.5,
    "barely": 0.4, "hardly": 0.4,
}


def lookup(word: str):
    """Return (polarity, base_weight) for *word*, or ``None``."""
    w = word.lower()
    if w in POSITIVE:
        return ("positive", POSITIVE[w])
    if w in NEGATIVE:
        return ("negative", NEGATIVE[w])
    return None


def stats():
    return {
        "positive": len(POSITIVE),
        "negative": len(NEGATIVE),
        "negators": len(NEGATORS),
        "intensifiers": len(INTENSIFIERS),
    }
