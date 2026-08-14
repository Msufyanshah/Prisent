# backend/app/routes/linkedin_auth.py
import secrets
import uuid
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db, get_utc_now
from app.models.user import User
from app.routes.auth import require_auth
from app.services.linkedin_oauth import (
    get_authorization_url, exchange_code_for_token, get_linkedin_profile
)
from app.services.encryption import encrypt_token
from app.utils.envelope import EnvelopedRoute


from app.config import settings
from app.services.redis_client import get_redis

router = APIRouter(prefix="/auth/linkedin", tags=["linkedin-auth"], route_class=EnvelopedRoute)


@router.get("/connect")
async def linkedin_connect(current_user: User = Depends(require_auth)):
    state = secrets.token_urlsafe(24)
    r = await get_redis()
    await r.setex(f"oauth_state:{state}", 600, str(current_user.id))
    await r.aclose()
    auth_url = get_authorization_url(state)
    return {"redirect_url": auth_url}

@router.get("/callback")
async def linkedin_callback(
    code: str = Query(None),
    state: str = Query(None),
    error: str = Query(None),
    error_description: str = Query(None),
    db: AsyncSession = Depends(get_db)
):
    frontend_url = "http://localhost:3000"
    if settings.ALLOWED_ORIGINS:
        frontend_url = settings.ALLOWED_ORIGINS[0]

    if error:
        return RedirectResponse(url=f"{frontend_url}/dashboard/settings?connected=false&error={error_description or error}")

    if not state:
        raise HTTPException(
            status_code=400,
            detail={"code": "INVALID_STATE", "message": "Missing state parameter"}
        )

    r = await get_redis()
    redis_key = f"oauth_state:{state}"
    user_id_bytes = await r.get(redis_key)
    if user_id_bytes:
        await r.delete(redis_key)
    await r.aclose()

    if not user_id_bytes:
        raise HTTPException(
            status_code=400,
            detail={"code": "INVALID_STATE", "message": "OAuth state mismatch or expired"}
        )
    user_id = user_id_bytes.decode("utf-8")

    if not code:
        raise HTTPException(
            status_code=400,
            detail={"code": "BAD_REQUEST", "message": "Authorization code is required"}
        )

    try:
        token_data = await exchange_code_for_token(code)
        access_token = token_data["access_token"]
        expires_in = token_data.get("expires_in", 5184000)
        profile = await get_linkedin_profile(access_token)
    except Exception as e:
        raise HTTPException(
            status_code=502,
            detail={"code": "OAUTH_FAILED", "message": str(e)}
        )

    try:
        user_uuid = uuid.UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail={"code": "INVALID_USER_ID", "message": "Invalid user ID format"}
        )

    result = await db.execute(select(User).where(User.id == user_uuid))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=404,
            detail={"code": "USER_NOT_FOUND", "message": "User not found"}
        )

    user.linkedin_access_token = encrypt_token(access_token)
    user.linkedin_token_expiry = get_utc_now() + timedelta(seconds=expires_in)
    user.linkedin_person_id = profile.get("sub")
    user.linkedin_display_name = profile.get("name", "Connected User")
    await db.commit()

    frontend_url = "http://localhost:3000"
    if settings.ALLOWED_ORIGINS:
        frontend_url = settings.ALLOWED_ORIGINS[0]
    return RedirectResponse(url=f"{frontend_url}/dashboard/settings?connected=true")

@router.get("/status")
async def linkedin_status(current_user: User = Depends(require_auth)):
    connected = current_user.linkedin_access_token is not None
    return {
        "connected": connected,
        "linkedin_name": current_user.linkedin_display_name if connected else None
    }

@router.post("/disconnect")
async def linkedin_disconnect(
    current_user: User = Depends(require_auth),
    db: AsyncSession = Depends(get_db)
):
    current_user.linkedin_access_token = None
    current_user.linkedin_token_expiry = None
    current_user.linkedin_person_id = None
    current_user.linkedin_display_name = None
    await db.commit()
    return {"connected": False}

