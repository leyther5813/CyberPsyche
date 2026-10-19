from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session as DBSession
from typing import Dict, Any, Optional

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.session_schema import DecisionSubmissionDTO, DecisionOutcomeResponseDTO
from app.schemas.event_schema import BehaviourEventDTO
from app.services.session_service import (
    create_session, get_next_scenario, log_event,
    submit_decision, calculate_resilience_profile
)

router = APIRouter(prefix="/sessions", tags=["sessions"])

@router.post("", response_model=dict)
def start_session(
    payload: Optional[Dict[str, Any]] = Body(default={}),
    current_user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db)
):
    arm = payload.get("arm", "targeted") if payload else "targeted"
    form_assignment = payload.get("form_assignment", "Form_A") if payload else "Form_A"
    session = create_session(db, user_id=current_user.id, arm=arm, form_assignment=form_assignment)
    return {
        "session_id": session.id,
        "arm": session.arm,
        "form_assignment": session.form_assignment,
        "current_phase": session.current_phase,
        "status": "created"
    }

@router.get("/{id}/next", response_model=dict)
def fetch_next_scenario(
    id: str,
    current_user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db)
):
    return get_next_scenario(db, session_id=id, user_id=current_user.id)

@router.post("/{id}/events", response_model=dict)
def record_event(
    id: str,
    dto: BehaviourEventDTO,
    current_user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db)
):
    return log_event(db, session_id=id, user_id=current_user.id, event_dto=dto)

@router.post("/{id}/decision", response_model=DecisionOutcomeResponseDTO)
def record_decision(
    id: str,
    dto: DecisionSubmissionDTO,
    current_user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db)
):
    return submit_decision(db, session_id=id, user_id=current_user.id, dto=dto)

@router.get("/{id}/profile", response_model=dict)
def get_session_profile(
    id: str,
    current_user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db)
):
    return calculate_resilience_profile(db, session_id=id, user_id=current_user.id)
