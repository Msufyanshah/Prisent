# backend/app/routes/posts.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db, get_utc_now
from app.models.user import User
from app.models.post import Post
from app.routes.auth import require_auth
from app.schemas.post import ApprovePostRequest, PostResponse
from app.services.linkedin_publisher import publish_to_linkedin, LinkedInPublishError
from app.services.linkedin_token_check import LinkedInTokenExpired, LinkedInNotConnected
from app.utils.envelope import EnvelopedRoute
from uuid import UUID

router = APIRouter(prefix="/posts", tags=["posts"], route_class=EnvelopedRoute)

MIN_QUALITY_SCORE = 70

async def _get_owned_post(post_id: str, user: User, db: AsyncSession) -> Post:
    try:
        post_uuid = UUID(post_id) if isinstance(post_id, str) else post_id
    except ValueError:
        raise HTTPException(
            status_code=404,
            detail={"code": "POST_NOT_FOUND", "message": "Post not found"}
        )
    result = await db.execute(select(Post).where(Post.id == post_uuid, Post.user_id == user.id))
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(
            status_code=404,
            detail={"code": "POST_NOT_FOUND", "message": "Post not found"}
        )
    return post

@router.get("", response_model=list[PostResponse])
async def list_posts(
    status_filter: str = None,
    current_user: User = Depends(require_auth),
    db: AsyncSession = Depends(get_db)
):
    query = select(Post).where(Post.user_id == current_user.id)
    if status_filter:
        query = query.where(Post.status == status_filter)
    query = query.order_by(Post.created_at.desc())
    result = await db.execute(query)
    return result.scalars().all()

@router.get("/{post_id}", response_model=PostResponse)
async def get_post(
    post_id: str,
    current_user: User = Depends(require_auth),
    db: AsyncSession = Depends(get_db)
):
    return await _get_owned_post(post_id, current_user, db)

@router.post("/{post_id}/approve", response_model=PostResponse)
async def approve_post(
    post_id: str,
    body: ApprovePostRequest,
    current_user: User = Depends(require_auth),
    db: AsyncSession = Depends(get_db)
):
    post = await _get_owned_post(post_id, current_user, db)

    if post.quality_score is not None and post.quality_score < MIN_QUALITY_SCORE:
        raise HTTPException(
            status_code=400,
            detail={
                "code": "QUALITY_SCORE_TOO_LOW",
                "message": f"Quality score {post.quality_score} is below the {MIN_QUALITY_SCORE} threshold required to publish"
            }
        )

    post.status = "scheduled"
    scheduled_naive = body.scheduled_at.replace(tzinfo=None) if body.scheduled_at.tzinfo else body.scheduled_at
    post.scheduled_at = scheduled_naive
    await db.commit()
    return post

@router.post("/{post_id}/publish-now", response_model=PostResponse)
async def publish_now(
    post_id: str,
    current_user: User = Depends(require_auth),
    db: AsyncSession = Depends(get_db)
):
    post = await _get_owned_post(post_id, current_user, db)

    if post.quality_score is not None and post.quality_score < MIN_QUALITY_SCORE:
        raise HTTPException(
            status_code=400,
            detail={
                "code": "QUALITY_SCORE_TOO_LOW",
                "message": f"Quality score {post.quality_score} is below the {MIN_QUALITY_SCORE} threshold required to publish"
            }
        )

    try:
        linkedin_post_id = await publish_to_linkedin(current_user, post.content)
    except LinkedInTokenExpired:
        raise HTTPException(
            status_code=400,
            detail={"code": "LINKEDIN_TOKEN_EXPIRED", "message": "Reconnect LinkedIn to publish"}
        )
    except LinkedInNotConnected:
        raise HTTPException(
            status_code=400,
            detail={"code": "LINKEDIN_NOT_CONNECTED", "message": "Connect LinkedIn first"}
        )
    except LinkedInPublishError as e:
        post.status = "failed"
        post.failure_reason = str(e)
        await db.commit()
        raise HTTPException(
            status_code=502,
            detail={"code": "LINKEDIN_API_ERROR", "message": str(e)}
        )

    post.status = "published"
    post.linkedin_post_id = linkedin_post_id
    post.published_at = get_utc_now()
    await db.commit()
    return post
