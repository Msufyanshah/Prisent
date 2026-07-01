from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routes.health import router as health_router
from app.routes.auth import router as auth_router
from app.routes.persona import router as persona_router
from app.routes.generate import router as generate_router
from app.routes.linkedin_auth import router as linkedin_auth_router
from app.routes.posts import router as posts_router
from app.utils.envelope import http_exception_handler, validation_exception_handler
from fastapi.exceptions import RequestValidationError, HTTPException

app = FastAPI(
    title="AutoPost AI",
    version="1.0.0",
    description="Autonomous LinkedIn post generator"
)

app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(persona_router)
app.include_router(generate_router)
app.include_router(linkedin_auth_router)
app.include_router(posts_router)

@app.get("/")
async def root():
    return {"message": "Welcome to AutoPost AI API"}

from app.services.qdrant_setup import create_collections

@app.on_event("startup")
async def startup():
    create_collections()
    print(f"AutoPost AI starting — env: {settings.ENV}")
