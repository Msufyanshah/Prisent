from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.user import User
from app.routes.auth import require_auth
from app.schemas.persona import SeedPostsRequest, SeedPostsResponse
from app.services.qdrant_client import upsert_batch, count_user_documents
from app.utils.envelope import EnvelopedRoute

router = APIRouter(prefix="/persona", tags=["persona"], route_class=EnvelopedRoute)

MIN_POSTS_REQUIRED = 3

@router.post("/seed-posts", response_model=SeedPostsResponse)
async def seed_posts(
    body: SeedPostsRequest,
    current_user: User = Depends(require_auth),
    db: AsyncSession = Depends(get_db)
):
    if len(body.posts) < MIN_POSTS_REQUIRED:
        raise HTTPException(
            status_code=400,
            detail={
                "code": "MIN_POSTS_NOT_MET",
                "message": f"Please provide at least {MIN_POSTS_REQUIRED} past posts to seed your voice memory."
            }
        )

    documents = [
        {
            "content": post.content,
            "type": "past_post",
            "metadata": {
                "approximate_date": post.approximate_date,
                "pillar": "general"
            }
        }
        for post in body.posts
    ]

    indexed = 0
    failed = 0
    try:
        await upsert_batch(str(current_user.id), documents)
        indexed = len(documents)
    except Exception as e:
        failed = len(documents)

    total = await count_user_documents(str(current_user.id))
    return SeedPostsResponse(indexed=indexed, failed=failed, total_in_memory=total)
