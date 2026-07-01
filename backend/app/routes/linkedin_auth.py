# backend/app/routes/linkedin_auth.py
import secrets
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Query
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

import redis.asyncio as aioredis
from app.config import settings

router = APIRouter(prefix="/auth/linkedin", tags=["linkedin-auth"], route_class=EnvelopedRoute)

async def get_redis():
    return await aioredis.from_url(settings.REDIS_URL)

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
    code: str = Query(...),
    state: str = Query(...),
    db: AsyncSession = Depends(get_db)
):
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

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=404,
            detail={"code": "USER_NOT_FOUND", "message": "User not found"}
        )

    user.linkedin_access_token = encrypt_token(access_token)
    user.linkedin_token_expiry = get_utc_now() + timedelta(seconds=expires_in)
    user.linkedin_person_id = profile.get("sub")
    await db.commit()

    return {"connected": True, "linkedin_name": profile.get("name")}
