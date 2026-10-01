"""Test suite for SentimentScope. Run:  python3 -m pytest"""

import pytest

from sentimentscope import analyze, label, score
from sentimentscope.alerts import detect
from sentimentscope.data import aggregate_daily, load_posts
from sentimentscope.lexicon import INTENSIFIERS, NEGATORS, lookup, stats


# ---------------------------------------------------------------- lexicon
def test_lexicon_sizes():
    s = stats()
    assert s["positive"] >= 200, s
    assert s["negative"] >= 200, s


def test_lexicon_lookup_polarity():
    assert lookup("fantastic")[0] == "positive"
    assert lookup("atrocious")[0] == "negative"
    assert lookup("quux-not-a-word") is None


# ------------------------------------------------------------- engine core
def test_plain_positive():
    assert score("I love this") > 0
    assert label("I love this") == "positive"


def test_plain_negative():
    assert score("This is terrible") < 0
    assert label("This is terrible") == "negative"


def test_neutral_text_scores_near_zero():
    for text in [
        "The coffee was served at noon.",
        "It arrived on Tuesday in a box.",
        "The meeting lasted forty minutes.",
    ]:
        assert score(text) == pytest.approx(0.0, abs=1e-9), text


# --------------------------------------------------------------- negation
def test_not_good_scores_negative():
    assert label("not good") == "negative"
    assert score("not good") < 0


def test_negated_negative_is_positive():
    assert label("not bad at all") == "positive"


def test_contraction_negates():
    assert label("don't love it") == "negative"


def test_negation_does_not_cross_sentence():
    # "awful" is in a new sentence, outside the negation scope
    r = analyze("not the best. Absolutely awful!")
    assert r["score"] < 0


def test_negation_scope_is_limited():
    # negator reaches ~3 tokens: "good" is hit, "great" far later is not
    r = analyze("not good in any way shape or form but honestly great")
    tokens = dict(r["tokens"])
    assert tokens["good"] < 0
    assert tokens["great"] > 0


# ------------------------------------------------------------ intensifiers
def test_intensifier_amplifies():
    assert score("very good") > score("good") > 0


def test_strong_intensifier_amplifies_more():
    assert score("extremely good") > score("very good")


def test_diminisher_dampens():
    # "slightly annoyed" is still negative, but closer to zero than "annoyed"
    assert score("annoyed") < score("slightly annoyed") < 0


def test_negation_and_intensifier_combine():
    # "not very good" should be MORE negative than "not good"
    assert score("not very good") < score("not good") < 0


# ---------------------------------------------------------------- emphasis
def test_caps_amplifies():
    assert abs(score("TERRIBLE")) > abs(score("terrible"))


def test_exclamation_amplifies():
    assert score("awful!") < score("awful") < 0


def test_analyze_trace_shape():
    r = analyze("very good")
    assert set(r) == {"text", "score", "label", "raw", "tokens"}
    assert -1.0 <= r["score"] <= 1.0
    assert r["label"] in {"positive", "negative", "neutral"}
    assert r["tokens"] == [("good", pytest.approx(1.5))]


# ------------------------------------------------------------ aggregation
@pytest.fixture(scope="module")
def daily():
    return aggregate_daily(load_posts())


def test_aggregation_covers_all_brand_days(daily):
    assert len(daily) == 21  # 3 brands x 7 days
    brands = {r["brand"] for r in daily}
    assert brands == {"VoltBean Coffee", "Nimbus Airlines", "PixelNest Games"}


def test_aggregation_row_invariants(daily):
    for r in daily:
        assert r["volume"] == r["pos"] + r["neu"] + r["neg"]
        assert -1.0 <= r["avg_score"] <= 1.0
        assert 0.0 <= r["neg_share"] <= 1.0


# ----------------------------------------------------------------- alerts
def test_spike_detector_fires_on_scripted_incident(daily):
    alerts = detect(daily)
    nimbus = [a for a in alerts if a["brand"] == "Nimbus Airlines"
              and a["date"] == "2026-09-25"]
    types = {a["type"] for a in nimbus}
    assert "sentiment_drop" in types
    assert "negative_surge" in types
    assert all(a["severity"] == "high" for a in nimbus)


def test_no_false_positives_on_quiet_brands(daily):
    alerts = detect(daily)
    for a in alerts:
        assert not (a["brand"] in {"VoltBean Coffee", "PixelNest Games"}), a


def test_alerts_are_configurable(daily):
    # impossibly strict thresholds -> silence
    strict = {"sentiment_drop_threshold": 5.0,
              "negative_surge_threshold": 5.0, "min_volume": 1}
    assert detect(daily, strict) == []


def test_min_volume_guards_noisy_days(daily):
    cfg = {"sentiment_drop_threshold": 0.01, "negative_surge_threshold": 0.01,
           "min_volume": 10_000}
    assert detect(daily, cfg) == []
