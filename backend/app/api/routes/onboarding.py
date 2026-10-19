import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session as DBSession

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User, Consent, DigitalContext
from app.schemas.user_schema import ConsentDTO, DigitalContextDTO

router = APIRouter(tags=["onboarding"])

@router.post("/consent", response_model=dict)
def accept_consent(
    dto: ConsentDTO,
    current_user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db)
):
    if not dto.accepted:
        raise HTTPException(status_code=400, detail="Consent must be accepted to participate in study")

    existing = db.query(Consent).filter(Consent.user_id == current_user.id).first()
    if not existing:
        consent = Consent(
            id=str(uuid.uuid4()),
            user_id=current_user.id,
            version=dto.version,
            accepted_at=datetime.now(timezone.utc)
        )
        db.add(consent)
        db.commit()

    return {"status": "accepted", "user_id": current_user.id, "version": dto.version}

@router.put("/context", response_model=dict)
def update_context(
    dto: DigitalContextDTO,
    current_user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db)
):
    context = db.query(DigitalContext).filter(DigitalContext.user_id == current_user.id).first()
    if not context:
        context = DigitalContext(
            id=str(uuid.uuid4()),
            user_id=current_user.id,
            life_stage=dto.life_stage,
            activities=dto.activities,
            cyber_level=dto.cyber_level,
            interests=dto.interests
        )
        db.add(context)
    else:
        context.life_stage = dto.life_stage
        context.activities = dto.activities
        context.cyber_level = dto.cyber_level
        context.interests = dto.interests

    db.commit()
    return {"status": "updated", "user_id": current_user.id}
