import asyncio
from datetime import datetime, timedelta
from sqlalchemy import select
from app.tasks.celery_app import celery_app
from app.database import AsyncSessionLocal
from app.models.post import Post
from app.models.user import User
from app.services.linkedin_analytics import fetch_post_analytics, LinkedInAnalyticsError

async def _sync_analytics():
    async with AsyncSessionLocal() as db:
        cutoff = datetime.utcnow() - timedelta(days=30)
        result = await db.execute(
            select(Post).where(
                Post.status == "published",
                Post.published_at >= cutoff
            )
        )
        posts = result.scalars().all()

        synced = 0
        failed = 0

        for post in posts:
            user_result = await db.execute(select(User).where(User.id == post.user_id))
            user = user_result.scalar_one_or_none()
            if not user or not post.linkedin_post_id:
                continue

            try:
                metrics = await fetch_post_analytics(user, post.linkedin_post_id)
                post.impressions = metrics["impressions"]
                post.reactions = metrics["reactions"]
                post.comments = metrics["comments"]
                post.reposts = metrics["reposts"]
                synced += 1
            except LinkedInAnalyticsError:
                failed += 1

        await db.commit()
        return {"synced": synced, "failed": failed, "total_checked": len(posts)}

@celery_app.task(name="sync_linkedin_analytics")
def sync_linkedin_analytics():
    return asyncio.run(_sync_analytics())
