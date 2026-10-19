from fastapi import APIRouter, Depends, Body, HTTPException
from sqlalchemy.orm import Session as DBSession
from typing import Dict, Any, Optional

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.services.session_service import get_intervention_content, complete_intervention

router = APIRouter(tags=["interventions"])

@router.get("/sessions/{id}/intervention", response_model=dict)
def fetch_intervention(
    id: str,
    current_user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db)
):
    return get_intervention_content(db, session_id=id, user_id=current_user.id)

@router.post("/intervention/complete", response_model=dict)
def finish_intervention(
    payload: Optional[Dict[str, Any]] = Body(default={}),
    current_user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db)
):
    session_id = payload.get("session_id") if payload else None
    practice_score = payload.get("practice_score", 100) if payload else 100
    if not session_id:
        raise HTTPException(status_code=400, detail="session_id is required")
        
    return complete_intervention(db, session_id=session_id, user_id=current_user.id, practice_score=practice_score)
