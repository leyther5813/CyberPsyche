from typing import List, Dict, Any, Optional
from statistics import mean

def select_targeted_intervention(baseline_outcomes: List[Dict[str, Any]]) -> str:
    """
    Robust Weakness Selector Algorithm for CyberPsyche Targeted Micro-Interventions.
    
    Identifies the participant's weakest decision mechanism or behavioral pattern
    from Phase 1 (Baseline) outcomes.
    
    Rules:
    1. Low verification overall (< 0.33) -> LESSON_LOW_VERIFICATION
    2. Mechanism vulnerability below 0.6 threshold -> LESSON_AUTH_VULNERABILITY / LESSON_URG_VULNERABILITY / LESSON_REW_VULNERABILITY
       (Only mechanisms with >= 1 observation are evaluated; empty mechanism subsets are safely ignored).
    3. High over-caution (>= 2 over-caution occurrences) -> LESSON_OVER_CAUTION
    4. Default fallback -> LESSON_GENERAL_STRATEGY
    """
    if not baseline_outcomes:
        return "LESSON_GENERAL_STRATEGY"

    # 1. Evaluate overall verification rate
    verification_rate = mean([1.0 if o.get("verified", False) else 0.0 for o in baseline_outcomes])
    if verification_rate < 0.33:
        return "LESSON_LOW_VERIFICATION"

    # 2. Evaluate mechanism-specific decision quality safely
    auth_scores = [o.get("decision_quality", 0.0) for o in baseline_outcomes if "authority" in o.get("mechanisms", [])]
    urg_scores = [o.get("decision_quality", 0.0) for o in baseline_outcomes if "urgency" in o.get("mechanisms", [])]
    rew_scores = [o.get("decision_quality", 0.0) for o in baseline_outcomes if "reward_scarcity" in o.get("mechanisms", [])]

    mech_means: Dict[str, float] = {}
    if auth_scores:
        mech_means["LESSON_AUTH_VULNERABILITY"] = mean(auth_scores)
    if urg_scores:
        mech_means["LESSON_URG_VULNERABILITY"] = mean(urg_scores)
    if rew_scores:
        mech_means["LESSON_REW_VULNERABILITY"] = mean(rew_scores)

    # If mechanism observations exist, find the weakest mechanism below 0.6 threshold
    if mech_means:
        weakest_lesson, lowest_score = min(mech_means.items(), key=lambda item: item[1])
        if lowest_score < 0.6:
            return weakest_lesson

    # 3. Evaluate over-caution frequency
    over_caution_count = sum([1 for o in baseline_outcomes if o.get("over_caution", False)])
    if over_caution_count >= 2:
        return "LESSON_OVER_CAUTION"

    # 4. Default fallback
    return "LESSON_GENERAL_STRATEGY"
