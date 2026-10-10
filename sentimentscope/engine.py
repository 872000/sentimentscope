"""Lexicon-based sentiment scoring engine — implemented from scratch.

Scoring rules (see module docstring for the lexicon itself):

1. **Tokenisation** — lowercase, split on whitespace/punctuation, keep
   apostrophes. Negation contractions are expanded first
   (``"don't"`` → ``"do not"``) so ``"n't"`` forms always negate.
2. **Base score** — every lexicon word contributes ``±base_weight``
   (``+1.0`` / ``-1.0`` standard, ``+2.0`` / ``-2.0`` strong).
3. **Intensifiers** — ``very`` ×1.5, ``extremely`` ×2.0, ``slightly`` ×0.5,
   … (see ``INTENSIFIERS``). They attach to the *next* sentiment token and
   stack multiplicatively (``"very very good"`` = 1.0 × 1.5 × 1.5).
   Diminishers (``barely``, ``hardly``, …) use factors < 1.
4. **Negation** — a negator (``not``, ``never``, ``no``, …) flips the sign
   of every sentiment token inside a **3-token forward scope**, and the
   flipped value is dampened ×0.7, because negated sentiment is weaker
   than the direct opposite (``"not terrible"`` ≈ mildly good, not great).
   Scope ends early at sentence-ending punctuation (``. ! ?``).
5. **Emphasis** — ALL-CAPS sentiment words get ×1.25 (shouting); a trailing
   ``!`` boosts the final magnitude ×1.15 (``!!…`` → ×1.25).
6. **Normalisation** — ``score = raw / (|raw| + 2)``. This keeps 0 at 0,
   maps ``±1 → ±0.33``, ``±5 → ±0.71`` and asymptotes to ``±1`` so a few
   strong words can't saturate the scale the way raw sums do.
7. **Labels** — ``score ≥ +0.25`` → ``positive``, ``score ≤ -0.25`` →
   ``negative``, otherwise ``neutral``.

Everything runs offline; the only state is the hand-built lexicon.
"""

from __future__ import annotations

import math
import re

from .lexicon import INTENSIFIERS, NEGATION_CONTRACTIONS, NEGATORS, lookup

# Configurable knobs (also documented in README)
NEGATION_SCOPE_TOKENS = 3   # how far a negator reaches forward
NEGATED_DAMPENING = 0.7     # negated sentiment is weaker than direct opposite
CAPS_MULTIPLIER = 1.25      # ALL-CAPS sentiment word emphasis
EXCLAIM_MULTIPLIER = 1.15   # trailing "!" emphasis
EXCLAIM_STRONG_MULTIPLIER = 1.25  # trailing "!!" or more
POSITIVE_THRESHOLD = 0.25
NEGATIVE_THRESHOLD = -0.25

_TOKEN_RE = re.compile(r"[A-Za-z']+|[.!?]+")
_SENTENCE_END = {".", "!", "?"}


def tokenize(text: str) -> list[str]:
    """Split *text* into word/punctuation tokens with contractions expanded.

    Returns the original-cased word tokens (caps matter for emphasis) and
    punctuation tokens. ``"Don't"`` becomes ``["Do", "not"]``.
    """
    expanded = text
    for contraction, replacement in NEGATION_CONTRACTIONS.items():
        expanded = re.sub(
            rf"\b{re.escape(contraction)}\b", replacement, expanded,
            flags=re.IGNORECASE,
        )
    # keep a capitalised copy of the expansion word for caps detection
    return _TOKEN_RE.findall(expanded)


def _is_shouted(token: str) -> bool:
    return token.isalpha() and token.isupper() and len(token) > 1


def analyze(text: str) -> dict:
    """Score *text* and return a full trace.

    Returns ``{"text", "score", "label", "raw", "tokens"}`` where ``tokens``
    is a list of ``(token, contribution)`` for sentiment-bearing tokens.
    """
    if not isinstance(text, str):
        raise TypeError(
            f"analyze() expects a string, got {type(text).__name__}"
        )
    tokens = tokenize(text)
    contributions: list[tuple[str, float]] = []
    raw = 0.0

    neg_scope = 0          # remaining tokens in negation scope
    intensifier = 1.0      # pending multiplier for next sentiment token
    intensifier_pending = False

    for token in tokens:
        if token in _SENTENCE_END:
            neg_scope = 0          # negation never crosses a sentence
            intensifier = 1.0
            intensifier_pending = False
            continue

        word = token.lower()

        if word in NEGATORS:
            neg_scope = NEGATION_SCOPE_TOKENS
            continue

        if word in INTENSIFIERS:
            if intensifier_pending:
                intensifier *= INTENSIFIERS[word]
            else:
                intensifier = INTENSIFIERS[word]
                intensifier_pending = True
            # intensifier itself consumes one negation-scope slot if active
            if neg_scope:
                neg_scope -= 1
            continue

        hit = lookup(word)
        if hit is None:
            if neg_scope:
                neg_scope -= 1     # non-sentiment words still consume scope
            intensifier = 1.0
            intensifier_pending = False
            continue

        polarity, weight = hit
        # NEGATIVE stores weights as negative by convention; use the
        # magnitude and let polarity own the sign.
        sign = 1.0 if polarity == "positive" else -1.0
        value = sign * abs(weight) * (intensifier if intensifier_pending else 1.0)
        if neg_scope:
            value = -value * NEGATED_DAMPENING
            neg_scope -= 1
        if _is_shouted(token):
            value *= CAPS_MULTIPLIER
        raw += value
        contributions.append((token, round(value, 4)))
        intensifier = 1.0
        intensifier_pending = False

    # trailing-exclamation emphasis on the final magnitude
    stripped = text.rstrip()
    exclaim = 0
    for ch in reversed(stripped):
        if ch == "!":
            exclaim += 1
        else:
            break
    if exclaim == 1:
        raw *= EXCLAIM_MULTIPLIER
    elif exclaim >= 2:
        raw *= EXCLAIM_STRONG_MULTIPLIER

    score = raw / (abs(raw) + 2.0) if raw else 0.0
    if score >= POSITIVE_THRESHOLD:
        label = "positive"
    elif score <= NEGATIVE_THRESHOLD:
        label = "negative"
    else:
        label = "neutral"

    return {
        "text": text,
        "score": round(score, 4),
        "label": label,
        "raw": round(raw, 4),
        "tokens": contributions,
    }


def score(text: str) -> float:
    """Convenience: just the normalised score for *text*."""
    return analyze(text)["score"]


def label(text: str) -> str:
    """Convenience: just the label for *text*."""
    return analyze(text)["label"]
