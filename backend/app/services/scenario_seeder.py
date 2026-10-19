import os
import json
import glob
from sqlalchemy.orm import Session
from app.models.scenario import Scenario, EvidenceItem

SCENARIOS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "scenarios", "set_v1")

def seed_scenarios(db: Session) -> int:
    """
    Seeds the database with frozen JSON scenarios from set_v1 if not already loaded.
    Returns the count of scenarios seeded.
    """
    json_files = glob.glob(os.path.join(SCENARIOS_DIR, "*.json"))
    seeded_count = 0

    for filepath in json_files:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        scenario_id = data["scenario_id"]
        existing = db.query(Scenario).filter(Scenario.id == scenario_id).first()
        if existing:
            continue

        scenario = Scenario(
            id=scenario_id,
            family_id=data["family_id"],
            phase_pool=data["phase_pool"],
            context=data["context"],
            channel=data["channel"],
            persona=data.get("persona", ""),
            truth=data["truth"],
            mechanisms=data["mechanisms"],
            pressure=data["pressure"],
            difficulty=data["difficulty"],
            json_payload=data,
            version=data.get("version", "scenario_set_v1")
        )
        db.add(scenario)

        for ev in data.get("evidence", []):
            ev_id = f"{scenario_id}-{ev['id']}"
            evidence = EvidenceItem(
                id=ev_id,
                scenario_id=scenario_id,
                label=ev["label"],
                value=ev["value"],
                signal=ev["signal"],
                diagnosticity=ev["diagnosticity"],
                official_channel=ev.get("official_channel", False)
            )
            db.add(evidence)
            
        seeded_count += 1

    if seeded_count > 0:
        db.commit()

    return seeded_count
