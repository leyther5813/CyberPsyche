from fastapi import APIRouter
from app.api.routes import auth, onboarding, sessions, interventions, research, privacy

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth.router)
api_router.include_router(onboarding.router)
api_router.include_router(sessions.router)
api_router.include_router(interventions.router)
api_router.include_router(research.router)
api_router.include_router(privacy.router)
