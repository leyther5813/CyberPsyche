from typing import List, Dict, Any

def calculate_decision_quality(action: str, safe_actions: List[str], acceptable_actions: List[str], unsafe_actions: List[str]) -> float:
    """
    Calculates decision quality:
    - 1.0 if action is safe
    - 0.5 if action is acceptable
    - 0.0 if action is unsafe
    """
    act = action.strip().upper() if isinstance(action, str) else action
    safe = [s.strip().upper() for s in safe_actions]
    acceptable = [a.strip().upper() for a in acceptable_actions]
    unsafe = [u.strip().upper() for u in unsafe_actions]

    if act in safe:
        return 1.0
    elif act in acceptable:
        return 0.5
    elif act in unsafe:
        return 0.0
    return 0.0

def calculate_under_caution(truth: str, action: str, unsafe_actions: List[str], official_channel_inspected: bool) -> bool:
    """
    Under-caution occurs when:
    - truth is malicious and action is unsafe
    - truth is ambiguous and action is PROCEED without official channel verification
    """
    act = action.strip().upper() if isinstance(action, str) else action
    unsafe = [u.strip().upper() for u in unsafe_actions]

    if truth == "malicious" and act in unsafe:
        return True
    if truth == "ambiguous" and act == "PROCEED" and not official_channel_inspected:
        return True
    return False

def calculate_over_caution(truth: str, action: str, evidence_opened_count: int) -> bool:
    """
    Over-caution occurs when:
    - truth is genuine and action is IGNORE or REPORT and evidence inspected < 2
    """
    act = action.strip().upper() if isinstance(action, str) else action
    if truth == "genuine" and act in ["IGNORE", "REPORT"] and evidence_opened_count < 2:
        return True
    return False

def calculate_independent_verification(action: str, official_channel_inspected: bool) -> bool:
    """
    Independent verification occurs when:
    - action is VERIFY_INDEPENDENTLY OR official_channel evidence item was inspected before deciding
    """
    act = action.strip().upper() if isinstance(action, str) else action
    if act == "VERIFY_INDEPENDENTLY" or official_channel_inspected:
        return True
    return False

def calculate_evidence_depth(opened_count: int, total_count: int) -> float:
    """
    Calculates evidence seeking depth ratio: opened / total.
    """
    if total_count <= 0:
        return 0.0
    return round(min(opened_count / total_count, 1.0), 4)

def calculate_reason_alignment(reason_tags: List[str], verified: bool) -> bool:
    """
    Checks for contradiction between verification reason tags and actual verified behavior.
    If participant selects a verification-related reasoning tag but did NOT independently verify,
    a contradiction flag (False) is returned.
    """
    verification_tags = [
        "Requires verification on official institutional portal",
        "I verified independently"
    ]
    
    has_verification_claim = any(tag in reason_tags for tag in verification_tags)
    if has_verification_claim and not verified:
        return False
    return True
