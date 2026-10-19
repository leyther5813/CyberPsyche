import pytest
from app.intervention.selector import select_targeted_intervention

def test_select_low_verification():
    # Low verification overall (< 0.33) triggers LESSON_LOW_VERIFICATION regardless of other scores
    outcomes = [
        {"verified": False, "decision_quality": 0.5, "mechanisms": ["authority"], "over_caution": False},
        {"verified": False, "decision_quality": 0.5, "mechanisms": ["authority"], "over_caution": False},
        {"verified": False, "decision_quality": 0.5, "mechanisms": ["urgency"], "over_caution": False},
    ]
    assert select_targeted_intervention(outcomes) == "LESSON_LOW_VERIFICATION"

def test_select_mechanism_vulnerability():
    # Verification is high (>= 0.33), but authority decision quality is low (0.0 < 0.6)
    outcomes = [
        {"verified": True, "decision_quality": 0.0, "mechanisms": ["authority"], "over_caution": False},
        {"verified": True, "decision_quality": 0.0, "mechanisms": ["authority"], "over_caution": False},
        {"verified": True, "decision_quality": 1.0, "mechanisms": ["urgency"], "over_caution": False},
    ]
    assert select_targeted_intervention(outcomes) == "LESSON_AUTH_VULNERABILITY"

def test_select_over_caution():
    # Verification high, mechanism scores high (>= 0.6), but over_caution >= 2
    outcomes = [
        {"verified": True, "decision_quality": 1.0, "mechanisms": ["authority"], "over_caution": True},
        {"verified": True, "decision_quality": 1.0, "mechanisms": ["authority"], "over_caution": True},
        {"verified": True, "decision_quality": 1.0, "mechanisms": ["urgency"], "over_caution": False},
    ]
    assert select_targeted_intervention(outcomes) == "LESSON_OVER_CAUTION"

def test_empty_mechanism_subsets():
    # Baseline outcomes with NO reward_scarcity mechanism scenarios present
    # Should safely skip reward_scarcity without calling min/mean on empty list
    outcomes = [
        {"verified": True, "decision_quality": 0.8, "mechanisms": ["authority"], "over_caution": False},
        {"verified": True, "decision_quality": 0.8, "mechanisms": ["urgency"], "over_caution": False},
    ]
    assert select_targeted_intervention(outcomes) == "LESSON_GENERAL_STRATEGY"
