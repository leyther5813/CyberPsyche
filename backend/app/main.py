from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import SessionLocal, engine, Base
from app.api.router import api_router
from app.services.scenario_seeder import seed_scenarios

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ensure database tables exist
    Base.metadata.create_all(bind=engine)
    
    # Seed frozen scenario library on startup
    db = SessionLocal()
    try:
        seed_scenarios(db)
    finally:
        db.close()
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# CORS Middleware
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router)

@app.get("/")
def root():
    return {
        "title": settings.PROJECT_NAME,
        "version": "1.0",
        "description": "A Decision-Process Laboratory for Social-Engineering Resilience"
    }
