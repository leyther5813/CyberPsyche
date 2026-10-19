import pytest
from app.scoring.constructs import (
    calculate_decision_quality,
    calculate_under_caution,
    calculate_over_caution,
    calculate_independent_verification,
    calculate_evidence_depth,
    calculate_reason_alignment,
)
from app.scoring.sdt import calculate_sdt_metrics

def test_calculate_decision_quality():
    safe = ["VERIFY_INDEPENDENTLY", "REPORT", "IGNORE"]
    acceptable = ["GATHER_MORE_EVIDENCE", "ASK_TRUSTED_PERSON"]
    unsafe = ["PROCEED", "REPLY_TO_SENDER"]

    assert calculate_decision_quality("VERIFY_INDEPENDENTLY", safe, acceptable, unsafe) == 1.0
    assert calculate_decision_quality("REPORT", safe, acceptable, unsafe) == 1.0
    assert calculate_decision_quality("GATHER_MORE_EVIDENCE", safe, acceptable, unsafe) == 0.5
    assert calculate_decision_quality("PROCEED", safe, acceptable, unsafe) == 0.0
    assert calculate_decision_quality("REPLY_TO_SENDER", safe, acceptable, unsafe) == 0.0
    assert calculate_decision_quality("UNKNOWN", safe, acceptable, unsafe) == 0.0

def test_calculate_under_caution():
    unsafe = ["PROCEED", "REPLY_TO_SENDER"]

    # Malicious scenario with unsafe action -> Under-caution = True
    assert calculate_under_caution("malicious", "PROCEED", unsafe, official_channel_inspected=False) is True
    assert calculate_under_caution("malicious", "REPLY_TO_SENDER", unsafe, official_channel_inspected=True) is True
    assert calculate_under_caution("malicious", "VERIFY_INDEPENDENTLY", unsafe, official_channel_inspected=True) is False

    # Ambiguous scenario with PROCEED without official channel -> Under-caution = True
    assert calculate_under_caution("ambiguous", "PROCEED", unsafe, official_channel_inspected=False) is True
    assert calculate_under_caution("ambiguous", "PROCEED", unsafe, official_channel_inspected=True) is False

    # Genuine scenario -> Under-caution = False
    assert calculate_under_caution("genuine", "PROCEED", unsafe, official_channel_inspected=False) is False

def test_calculate_over_caution():
    # Genuine item rejected without sufficient evidence (< 2 items opened) -> Over-caution = True
    assert calculate_over_caution("genuine", "IGNORE", evidence_opened_count=0) is True
    assert calculate_over_caution("genuine", "REPORT", evidence_opened_count=1) is True
    assert calculate_over_caution("genuine", "REPORT", evidence_opened_count=2) is False
    assert calculate_over_caution("genuine", "PROCEED", evidence_opened_count=0) is False

    # Malicious or ambiguous item -> Over-caution = False
    assert calculate_over_caution("malicious", "IGNORE", evidence_opened_count=0) is False
    assert calculate_over_caution("ambiguous", "REPORT", evidence_opened_count=0) is False

def test_calculate_independent_verification():
    assert calculate_independent_verification("VERIFY_INDEPENDENTLY", official_channel_inspected=False) is True
    assert calculate_independent_verification("PROCEED", official_channel_inspected=True) is True
    assert calculate_independent_verification("PROCEED", official_channel_inspected=False) is False

def test_calculate_evidence_depth():
    assert calculate_evidence_depth(3, 6) == 0.5
    assert calculate_evidence_depth(6, 6) == 1.0
    assert calculate_evidence_depth(0, 6) == 0.0
    assert calculate_evidence_depth(0, 0) == 0.0

def test_calculate_reason_alignment():
    # Inconsistent: claiming verification without having verified
    assert calculate_reason_alignment(["I verified independently"], verified=False) is False
    assert calculate_reason_alignment(["I verified independently"], verified=True) is True
    assert calculate_reason_alignment(["Sender looked trustworthy"], verified=False) is True

def test_calculate_sdt_metrics():
    malicious = [
        {"under_caution": False},  # Hit
        {"under_caution": False},  # Hit
        {"under_caution": False},  # Hit
        {"under_caution": True},   # Miss
    ]
    genuine = [
        {"over_caution": False},   # Correct rejection
        {"over_caution": False},   # Correct rejection
        {"over_caution": True},    # False alarm
        {"over_caution": False},   # Correct rejection
    ]

    metrics = calculate_sdt_metrics(malicious, genuine)
    assert metrics["hit_rate"] == 0.75
    assert metrics["false_alarm_rate"] == 0.25
    assert metrics["d_prime"] > 0  # Sensitivity should be positive for good discrimination

def test_action_casing_and_whitespace_insensitivity():
    """Verify scoring functions handle lowercase and whitespace-padded action strings correctly."""
    safe = ["VERIFY_INDEPENDENTLY", "REPORT", "IGNORE"]
    acceptable = ["GATHER_MORE_EVIDENCE", "ASK_TRUSTED_PERSON"]
    unsafe = ["PROCEED", "REPLY_TO_SENDER"]

    # Lowercase & whitespace in calculate_decision_quality
    assert calculate_decision_quality("verify_independently", safe, acceptable, unsafe) == 1.0
    assert calculate_decision_quality("  verify_independently  ", safe, acceptable, unsafe) == 1.0
    assert calculate_decision_quality("gather_more_evidence", safe, acceptable, unsafe) == 0.5
    assert calculate_decision_quality("proceed", safe, acceptable, unsafe) == 0.0

    # Lowercase in calculate_under_caution
    assert calculate_under_caution("malicious", "proceed", unsafe, official_channel_inspected=False) is True
    assert calculate_under_caution("malicious", "verify_independently", unsafe, official_channel_inspected=True) is False
    assert calculate_under_caution("ambiguous", "proceed", unsafe, official_channel_inspected=False) is True
    assert calculate_under_caution("ambiguous", "proceed", unsafe, official_channel_inspected=True) is False

    # Lowercase in calculate_over_caution
    assert calculate_over_caution("genuine", "ignore", evidence_opened_count=0) is True
    assert calculate_over_caution("genuine", "report", evidence_opened_count=1) is True

    # Lowercase in calculate_independent_verification
    assert calculate_independent_verification("verify_independently", official_channel_inspected=False) is True
    assert calculate_independent_verification("  verify_independently  ", official_channel_inspected=False) is True

def test_decision_submission_dto_validation_and_normalization():
    """Verify DecisionSubmissionDTO normalizes action casing and rejects invalid actions."""
    from pydantic import ValidationError
    from app.schemas.session_schema import DecisionSubmissionDTO

    # Normalization of lowercase to uppercase
    dto = DecisionSubmissionDTO(
        scenario_id="TEST-01",
        action="verify_independently",
        reason_tags=["I verified independently"],
        confidence=4,
        latency_ms=1000
    )
    assert dto.action == "VERIFY_INDEPENDENTLY"

    # Whitespace stripping
    dto_ws = DecisionSubmissionDTO(
        scenario_id="TEST-01",
        action="  proceed  ",
        reason_tags=[],
        confidence=3,
        latency_ms=500
    )
    assert dto_ws.action == "PROCEED"

    # Invalid action rejected
    with pytest.raises(ValidationError):
        DecisionSubmissionDTO(
            scenario_id="TEST-01",
            action="invalid_unknown_action",
            reason_tags=[],
            confidence=3,
            latency_ms=500
        )

def test_hautus_correction_exact_values():
    """Verify Hautus (1995) log-linear correction with 2 hits / 2 mal and 0 FA / 3 gen yields d'=2.1178, c=0.0915."""
    malicious = [{"under_caution": False}, {"under_caution": False}]
    genuine = [{"over_caution": False}, {"over_caution": False}, {"over_caution": False}]
    metrics = calculate_sdt_metrics(malicious, genuine)
    assert metrics["d_prime"] == 2.1178
    assert metrics["criterion_c"] == 0.0915

def test_varied_behavioral_profiles_produce_distinct_metrics():
    """Verify that different behavioral patterns produce distinct d' and criterion c metrics."""
    # Gullible pattern: miss on malicious
    gullible = calculate_sdt_metrics([{"under_caution": True}, {"under_caution": True}], [{"over_caution": False}, {"over_caution": False}, {"over_caution": False}])
    # Paranoid pattern: false alarms on genuine
    paranoid = calculate_sdt_metrics([{"under_caution": False}, {"under_caution": False}], [{"over_caution": True}, {"over_caution": True}, {"over_caution": False}])
    # Calibrated pattern: hits on malicious, correct rejections on genuine
    calibrated = calculate_sdt_metrics([{"under_caution": False}, {"under_caution": False}], [{"over_caution": False}, {"over_caution": False}, {"over_caution": False}])

    assert gullible["d_prime"] != paranoid["d_prime"]
    assert gullible["d_prime"] != calibrated["d_prime"]
    assert gullible["criterion_c"] != paranoid["criterion_c"]
    assert calibrated["d_prime"] > gullible["d_prime"]

