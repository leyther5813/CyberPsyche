from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session as DBSession

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/privacy", tags=["privacy"])

@router.delete("/delete-me", response_model=dict)
def delete_user_account(
    current_user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db)
):
    user_id = current_user.id
    db.delete(current_user)
    db.commit()
    return {"status": "deleted", "user_id": user_id, "message": "All personal data successfully removed."}
