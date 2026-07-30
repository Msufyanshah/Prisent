from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.user import User
from app.models.post import Post
from app.routes.auth import require_auth
from app.schemas.analytics import AnalyticsSummary, PostAnalytics

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/summary", response_model=AnalyticsSummary)
async def get_summary(current_user: User = Depends(require_auth), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Post).where(Post.user_id == current_user.id, Post.status == "published")
    )
    posts = result.scalars().all()

    if not posts:
        return AnalyticsSummary(total_posts_published=0, avg_impressions=0, avg_reactions=0, avg_comments=0, best_pillar=None)

    total = len(posts)
    avg_impressions = sum(p.impressions for p in posts) / total
    avg_reactions = sum(p.reactions for p in posts) / total
    avg_comments = sum(p.comments for p in posts) / total

    pillar_scores: dict[str, list[int]] = {}
    for p in posts:
        if p.content_pillar:
            pillar_scores.setdefault(p.content_pillar, []).append(p.reactions + p.comments)
    best_pillar = max(pillar_scores, key=lambda k: sum(pillar_scores[k]) / len(pillar_scores[k])) if pillar_scores else None

    return AnalyticsSummary(
        total_posts_published=total,
        avg_impressions=round(avg_impressions, 1),
        avg_reactions=round(avg_reactions, 1),
        avg_comments=round(avg_comments, 1),
        best_pillar=best_pillar
    )

@router.get("/posts", response_model=list[PostAnalytics])
async def get_post_analytics(current_user: User = Depends(require_auth), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Post)
        .where(Post.user_id == current_user.id, Post.status == "published")
        .order_by(Post.published_at.desc())
    )
    posts = result.scalars().all()
    return [
        PostAnalytics(
            post_id=str(p.id),
            content_preview=p.content[:100],
            pillar=p.content_pillar,
            impressions=p.impressions,
            reactions=p.reactions,
            comments=p.comments,
            published_at=p.published_at.isoformat() if p.published_at else None
        )
        for p in posts
    ]
