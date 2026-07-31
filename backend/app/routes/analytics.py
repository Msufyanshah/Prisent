from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.user import User
from app.models.post import Post
from app.routes.auth import require_auth
from app.schemas.analytics import AnalyticsSummary, PostAnalytics
from app.config import settings

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

@router.get("/insight")
async def get_insight(current_user: User = Depends(require_auth), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Post).where(Post.user_id == current_user.id, Post.status == "published")
    )
    posts = result.scalars().all()

    if not posts:
        return {"insight": "No published posts yet. Once you publish content, your AI assistant will analyze performance trends to suggest optimizations."}

    # Format posts for LLM context
    context_lines = []
    for p in posts[:15]:  # Take up to 15 recent published posts
        context_lines.append(
            f"Pillar: {p.content_pillar or 'N/A'} | Likes: {p.reactions} | Comments: {p.comments}\nContent: {p.content[:150]}..."
        )
    posts_context = "\n---\n".join(context_lines)

    prompt = f"""
    You are an expert LinkedIn growth strategist. Analyze the performance of these recent posts:
    
    {posts_context}
    
    Provide exactly one brief paragraph (max 3 sentences) of highly actionable advice. Identify which topic or pillar is performing best and suggest a specific strategy the user should use for their next post to maximize engagement. Keep the tone professional, encouraging, and direct. Refer to specific data points if helpful.
    """

    from openai import AsyncOpenAI
    client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    try:
        completion = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a LinkedIn analytics growth advisor. Provide brief, actionable growth insights."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7
        )
        insight = completion.choices[0].message.content.strip()
    except Exception as e:
        insight = f"Failed to generate insight: {str(e)}. Keep posting to let our AI models find performance optimizations."

    return {"insight": insight}

