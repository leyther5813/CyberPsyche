import csv
import io
from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session as DBSession

from app.core.database import get_db
from app.api.deps import get_current_researcher
from app.models.user import User
from app.models.scenario import Scenario
from app.models.session import Session, SessionScenario
from app.models.behaviour import BehaviourEvent, Decision, ScenarioOutcome

router = APIRouter(prefix="/research", tags=["research"])

@router.get("/export")
def export_research_data(
    current_user: User = Depends(get_current_researcher),
    db: DBSession = Depends(get_db)
):
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Header containing all required research & statistical analysis dimensions
    writer.writerow([
        "session_id", "pseudonym_user_hash", "arm", "form_assignment", "completed_at",
        "decision_id", "scenario_id", "phase", "truth", "pressure", "mechanisms",
        "family_id", "context", "channel", "action", "confidence", "latency_ms",
        "decision_quality", "under_caution", "over_caution", "verified",
        "evidence_depth", "reason_alignment_flag"
    ])
    
    sessions = db.query(Session).all()
    for sess in sessions:
        user_hash = sess.user.email_hash if sess.user else "deleted"
        decisions = db.query(Decision).filter(Decision.session_id == sess.id).all()
        for dec in decisions:
            out = db.query(ScenarioOutcome).filter(ScenarioOutcome.decision_id == dec.id).first()
            ss = db.query(SessionScenario).filter(
                SessionScenario.session_id == sess.id,
                SessionScenario.scenario_id == dec.scenario_id
            ).first()
            sc = db.query(Scenario).filter(Scenario.id == dec.scenario_id).first()

            phase_val = ss.phase if ss else ""
            truth_val = sc.truth if sc else ""
            pressure_val = sc.pressure if sc else ""
            mechanisms_val = ",".join(sc.mechanisms) if (sc and sc.mechanisms) else ""
            family_val = sc.family_id if sc else ""
            context_val = sc.context if sc else ""
            channel_val = sc.channel if sc else ""

            writer.writerow([
                sess.id,
                user_hash,
                sess.arm,
                sess.form_assignment,
                sess.completed_at.isoformat() if sess.completed_at else "",
                dec.id,
                dec.scenario_id,
                phase_val,
                truth_val,
                pressure_val,
                mechanisms_val,
                family_val,
                context_val,
                channel_val,
                dec.action,
                dec.confidence,
                dec.latency_ms,
                out.decision_quality if out else "",
                out.under_caution if out else "",
                out.over_caution if out else "",
                out.verified if out else "",
                out.evidence_depth if out else "",
                out.reason_alignment_flag if out else ""
            ])
            
    csv_content = output.getvalue()
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=cyberpsyche_research_export.csv"}
    )
