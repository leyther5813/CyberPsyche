import os
import sys
import json
import glob
from typing import List, Dict, Any, Tuple

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pydantic import ValidationError
from app.schemas.scenario_schema import ScenarioBase

SCENARIOS_DIR = os.path.join(os.path.dirname(__file__), "..", "scenarios", "set_v1")

def validate_scenario_file(filepath: str) -> Tuple[bool, List[str]]:
    errors = []
    filename = os.path.basename(filepath)
    
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        return False, [f"Invalid JSON format in {filename}: {str(e)}"]

    # 1. Validate against Pydantic Schema
    try:
        scenario = ScenarioBase(**data)
    except ValidationError as ve:
        errors.append(f"Pydantic schema validation failed for {filename}: {ve.errors()}")
        return False, errors

    # 2. Check clue distribution rules per truth class
    truth = scenario.truth
    evidence = scenario.evidence

    if truth == "malicious":
        high_suspicious = [e for e in evidence if e.signal == "suspicious" and e.diagnosticity == "high"]
        trustworthy_clues = [e for e in evidence if e.signal == "trustworthy"]
        if len(high_suspicious) < 2:
            errors.append(f"{filename} (malicious): must contain at least 2 high-diagnosticity suspicious clues, found {len(high_suspicious)}")
        if len(trustworthy_clues) < 1:
            errors.append(f"{filename} (malicious): must contain at least 1 trustworthy clue, found {len(trustworthy_clues)}")

    elif truth == "genuine":
        official_channels = [e for e in evidence if e.official_channel]
        if len(official_channels) < 1:
            errors.append(f"{filename} (genuine): must contain at least 1 official_channel evidence item")

    elif truth == "ambiguous":
        high_suspicious = [e for e in evidence if e.signal == "suspicious" and e.diagnosticity == "high"]
        if len(high_suspicious) > 0:
            errors.append(f"{filename} (ambiguous): must not have a single high-diagnosticity resolving clue before official channel check")

    return len(errors) == 0, errors

def validate_scenario_set() -> Dict[str, Any]:
    json_files = glob.glob(os.path.join(SCENARIOS_DIR, "*.json"))
    results = {
        "total_files": len(json_files),
        "valid_files": 0,
        "errors": [],
        "truth_counts": {"malicious": 0, "genuine": 0, "ambiguous": 0},
        "pool_counts": {"baseline": 0, "retest": 0, "transfer": 0, "delayed": 0},
        "context_counts": {"education_career": 0, "finance": 0, "social_messaging": 0},
        "channel_counts": {"email": 0, "chat": 0},
        "mechanism_counts": {"authority": 0, "urgency": 0, "reward_scarcity": 0},
        "mechanism_combination_counts": {"AUTH": 0, "URG": 0, "REW": 0, "AUTH+URG": 0, "REW+URG": 0},
        "family_map": {}
    }

    for filepath in json_files:
        is_valid, errs = validate_scenario_file(filepath)
        if not is_valid:
            results["errors"].extend(errs)
        else:
            results["valid_files"] += 1
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            results["truth_counts"][data["truth"]] += 1
            results["pool_counts"][data["phase_pool"]] += 1
            results["context_counts"][data["context"]] += 1
            results["channel_counts"][data["channel"]] += 1
            for m in data["mechanisms"]:
                results["mechanism_counts"][m] += 1
                
            mechs = sorted(data["mechanisms"])
            if mechs == ["authority"]:
                results["mechanism_combination_counts"]["AUTH"] += 1
            elif mechs == ["urgency"]:
                results["mechanism_combination_counts"]["URG"] += 1
            elif mechs == ["reward_scarcity"]:
                results["mechanism_combination_counts"]["REW"] += 1
            elif mechs == ["authority", "urgency"]:
                results["mechanism_combination_counts"]["AUTH+URG"] += 1
            elif mechs == ["reward_scarcity", "urgency"]:
                results["mechanism_combination_counts"]["REW+URG"] += 1

            fam = data["family_id"]
            if fam not in results["family_map"]:
                results["family_map"][fam] = []
            results["family_map"][fam].append(data["scenario_id"])

    return results

if __name__ == "__main__":
    print("Running CyberPsyche Scenario Set Validation...")
    res = validate_scenario_set()
    print(f"Total scenarios found: {res['total_files']}")
    print(f"Valid scenarios: {res['valid_files']}")
    print(f"Truth distribution: {res['truth_counts']}")
    print(f"Pool distribution: {res['pool_counts']}")
    print(f"Context distribution: {res['context_counts']}")
    print(f"Channel distribution: {res['channel_counts']}")
    print(f"Individual Mechanism distribution: {res['mechanism_counts']}")
    print(f"Mechanism Combination distribution: {res['mechanism_combination_counts']}")
    print(f"Families matched: {len(res['family_map'])}")
    if res["errors"]:
        print("\nERRORS FOUND:")
        for err in res["errors"]:
            print(f" - {err}")
        sys.exit(1)
    else:
        print("\nAll scenarios PASSED schema and rule validation successfully!")
