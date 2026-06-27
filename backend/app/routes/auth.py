from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.user import User
from app.schemas.user import RegisterRequest, LoginRequest, AuthResponse
from app.services.auth import (
    hash_password, verify_password, create_access_token,
    get_user_by_email, get_current_user
)

from app.utils.envelope import EnvelopedRoute

router = APIRouter(prefix="/auth", tags=["auth"], route_class=EnvelopedRoute)
security = HTTPBearer()

@router.post("/register", response_model=AuthResponse, status_code=201)
async def register(body: RegisterRequest, db: AsyncSession = Depends(get_db)):
    existing = await get_user_by_email(db, body.email)
    if existing:
        raise HTTPException(
            status_code=400,
            detail={"code": "EMAIL_TAKEN", "message": "Email already registered"}
        )

    user = User(
        email=body.email,
        hashed_password=hash_password(body.password),
        name=body.name
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    token = create_access_token(str(user.id))
    return AuthResponse(user_id=str(user.id), token=token, name=user.name)

@router.post("/login", response_model=AuthResponse)
async def login(body: LoginRequest, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_email(db, body.email)
    if not user or not verify_password(body.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail={"code": "INVALID_CREDENTIALS", "message": "Invalid email or password"}
        )

    token = create_access_token(str(user.id))
    return AuthResponse(user_id=str(user.id), token=token, name=user.name)


# Reusable dependency for all protected routes
async def require_auth(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    user = await get_current_user(credentials.credentials, db)
    if not user:
        raise HTTPException(
            status_code=401,
            detail={"code": "UNAUTHORIZED", "message": "Invalid or expired token"}
        )
    return user
