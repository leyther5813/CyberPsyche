import hashlib
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session as DBSession

from app.core.database import get_db
from app.core.security import hash_password, verify_password, create_access_token
from app.models.user import User
from app.schemas.user_schema import UserRegisterDTO, UserLoginDTO, UserResponseDTO

router = APIRouter(prefix="/auth", tags=["auth"])

def hash_email(email: str) -> str:
    """Pseudonymizes user email via SHA-256 hash as specified in spec."""
    return hashlib.sha256(email.strip().lower().encode("utf-8")).hexdigest()

@router.post("/register", response_model=dict)
def register(dto: UserRegisterDTO, db: DBSession = Depends(get_db)):
    email_h = hash_email(dto.email)
    existing = db.query(User).filter(User.email_hash == email_h).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already registered")

    user = User(
        email_hash=email_h,
        password_hash=hash_password(dto.password),
        role="participant",
        created_at=datetime.now(timezone.utc)
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    access_token = create_access_token(subject=user.id, role=user.role)
    return {
        "user": UserResponseDTO(id=user.id, email_hash=user.email_hash, role=user.role).model_dump(),
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.post("/login", response_model=dict)
def login(dto: UserLoginDTO, db: DBSession = Depends(get_db)):
    email_h = hash_email(dto.email)
    user = db.query(User).filter(User.email_hash == email_h).first()
    if not user or not verify_password(dto.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token(subject=user.id, role=user.role)
    return {
        "user": UserResponseDTO(id=user.id, email_hash=user.email_hash, role=user.role).model_dump(),
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.post("/logout", response_model=dict)
def logout():
    return {"message": "Successfully logged out"}
