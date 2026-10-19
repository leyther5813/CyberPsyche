from typing import List, Dict, Tuple
from scipy.stats import norm

def calculate_sdt_metrics(malicious_outcomes: List[dict], genuine_outcomes: List[dict]) -> Dict[str, float]:
    """
    Calculates Signal Detection Theory (SDT) metrics:
    - Hit Rate (H): Malicious scenarios correctly defended (under_caution == False)
    - False Alarm Rate (FA): Genuine scenarios incorrectly rejected (over_caution == True)
    - Sensitivity (d'): d' = z(H) - z(FA)
    - Response Bias / Criterion (c): c = -0.5 * (z(H) + z(FA))
    
    Applies Log-linear correction (Hautus 1995) to prevent extreme 0 or 1 rates.
    """
    n_mal = len(malicious_outcomes)
    n_gen = len(genuine_outcomes)

    if n_mal == 0 or n_gen == 0:
        return {
            "hit_rate": 0.0,
            "false_alarm_rate": 0.0,
            "d_prime": 0.0,
            "criterion_c": 0.0
        }

    # Count hits: malicious defended correctly
    hits = sum([1 for o in malicious_outcomes if not o.get("under_caution", True)])
    
    # Count false alarms: genuine rejected incorrectly (over_caution == True)
    false_alarms = sum([1 for o in genuine_outcomes if o.get("over_caution", False)])

    # Log-linear adjustment for extreme rates
    h_adj = (hits + 0.5) / (n_mal + 1.0)
    fa_adj = (false_alarms + 0.5) / (n_gen + 1.0)

    # Calculate z-scores using inverse standard normal CDF (norm.ppf)
    z_h = float(norm.ppf(h_adj))
    z_fa = float(norm.ppf(fa_adj))

    d_prime = z_h - z_fa
    criterion_c = -0.5 * (z_h + z_fa)

    return {
        "hit_rate": round(hits / n_mal, 4),
        "false_alarm_rate": round(false_alarms / n_gen, 4),
        "d_prime": round(d_prime, 4),
        "criterion_c": round(criterion_c, 4)
    }
