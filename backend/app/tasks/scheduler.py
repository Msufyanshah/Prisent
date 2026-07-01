# backend/app/tasks/scheduler.py
import asyncio
from app.tasks.celery_app import celery_app
from app.database import AsyncSessionLocal, get_utc_now
from app.models.post import Post
from app.models.user import User
from app.services.linkedin_publisher import publish_to_linkedin, LinkedInPublishError
from app.services.linkedin_token_check import LinkedInTokenExpired, LinkedInNotConnected
from sqlalchemy import select

async def _publish_due_posts():
    async with AsyncSessionLocal() as db:
        now = get_utc_now()
        result = await db.execute(
            select(Post).where(
                Post.status == "scheduled",
                Post.scheduled_at <= now
            )
        )
        due_posts = result.scalars().all()

        published_count = 0
        failed_count = 0

        for post in due_posts:
            user_result = await db.execute(select(User).where(User.id == post.user_id))
            user = user_result.scalar_one_or_none()
            if not user:
                continue

            try:
                linkedin_post_id = await publish_to_linkedin(user, post.content)
                post.status = "published"
                post.linkedin_post_id = linkedin_post_id
                post.published_at = get_utc_now()
                published_count += 1
            except (LinkedInTokenExpired, LinkedInNotConnected, LinkedInPublishError) as e:
                post.status = "failed"
                post.failure_reason = str(e)
                failed_count += 1

        await db.commit()
        return {"published": published_count, "failed": failed_count, "checked": len(due_posts)}

@celery_app.task(name="publish_scheduled_posts")
def publish_scheduled_posts():
    """Runs every 5 minutes via Celery beat. Publishes any posts that are due."""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    if loop.is_running():
        future = asyncio.run_coroutine_threadsafe(_publish_due_posts(), loop)
        return future.result()
    else:
        return loop.run_until_complete(_publish_due_posts())
