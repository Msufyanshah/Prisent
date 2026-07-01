# backend/app/agents/orchestrator.py
import uuid
from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.persona import Persona
from app.models.post import Post
from app.models.agent_job import AgentJob
from app.agents.research_agent import run_research_agent
from app.agents.writer_agent import run_writer_agent
from app.agents.reviewer_agent import run_reviewer_agent
from app.services.qdrant_client import get_client, COLLECTION
from qdrant_client.models import Filter, FieldCondition, MatchValue
from app.database import get_utc_now

async def run_orchestrator(user_id: str, job_id: str, db: AsyncSession):
    """
    Chains Research -> Writer -> Reviewer agents together with auto-retries.
    Saves outputs to PostgreSQL tables.
    """
    job_uuid = uuid.UUID(job_id)
    user_uuid = uuid.UUID(user_id)
    
    result = await db.execute(select(AgentJob).where(AgentJob.id == job_uuid))
    job = result.scalar_one_or_none()
    if not job:
        return

    try:
        # Step 0: Check Persona
        result = await db.execute(select(Persona).where(Persona.user_id == user_uuid))
        persona_obj = result.scalar_one_or_none()
        if not persona_obj:
            job.status = "failed"
            job.progress_message = "Persona setup missing. Please set up a creator persona first."
            job.error = "PERSONA_NOT_FOUND"
            job.completed_at = get_utc_now()
            await db.commit()
            return

        # Step 0b: Check Voice Memory Count (min 3 past posts)
        try:
            client = get_client()
            count_res = client.count(
                collection_name=COLLECTION,
                count_filter=Filter(
                    must=[
                        FieldCondition(key="user_id", match=MatchValue(value=user_id)),
                        FieldCondition(key="type", match=MatchValue(value="past_post"))
                    ]
                )
            )
            past_post_count = count_res.count
        except Exception:
            # Fallback if Qdrant isn't initialized or crashes in test
            past_post_count = 0

        if past_post_count < 3:
            job.status = "failed"
            job.progress_message = f"Voice memory requires at least 3 past posts. Currently indexed: {past_post_count}."
            job.error = "VOICE_MEMORY_EMPTY"
            job.completed_at = get_utc_now()
            await db.commit()
            return

        # Step 1: Research Agent
        job.status = "researching"
        job.progress_message = "Analyzing market trends and selecting relevant LinkedIn topics..."
        await db.commit()
        await db.refresh(job)

        recent_topics = []
        research_res = await run_research_agent(
            niche=persona_obj.niche,
            content_pillars=persona_obj.content_pillars,
            target_audience=persona_obj.target_audience,
            avoid_topics=persona_obj.avoid_topics or [],
            recent_post_topics=recent_topics
        )

        if research_res.get("status") == "failed":
            job.status = "failed"
            job.progress_message = "Research Agent failed."
            job.error = research_res.get("reason", "Unknown error during research")
            job.completed_at = get_utc_now()
            await db.commit()
            return

        job.research_output = research_res
        await db.commit()
        await db.refresh(job)

        # Step 2: Writing & Review Loop (Max 2 retries)
        feedback = None
        reviewer_res = None
        writer_res = None
        retries = 0

        while retries <= 2:
            job.status = "writing"
            job.progress_message = f"Drafting post in your unique brand voice (attempt {retries + 1}/3)..."
            job.retries = retries
            await db.commit()
            await db.refresh(job)

            writer_res = await run_writer_agent(
                user_id=user_id,
                research=research_res,
                persona={
                    "tone": persona_obj.tone,
                    "content_goal": persona_obj.content_goal,
                    "unique_differentiator": persona_obj.unique_differentiator
                },
                feedback=feedback
            )

            if writer_res.get("status") == "failed":
                job.status = "failed"
                job.progress_message = "Writer Agent failed."
                job.error = writer_res.get("reason", "Unknown error during writing")
                job.completed_at = get_utc_now()
                await db.commit()
                return

            job.draft_content = writer_res.get("post_content")
            job.status = "reviewing"
            job.progress_message = "Evaluating content alignment and checking formatting rules..."
            await db.commit()
            await db.refresh(job)

            # Review Agent
            reviewer_res = await run_reviewer_agent(
                user_id=user_id,
                post_draft=writer_res,
                persona={
                    "tone": persona_obj.tone,
                    "content_pillars": persona_obj.content_pillars
                },
                retry_count=retries
            )

            job.quality_score = reviewer_res.get("quality_score", 0)
            job.review_notes = reviewer_res.get("notes") or reviewer_res.get("specific_feedback") or reviewer_res.get("reason")
            await db.commit()
            await db.refresh(job)

            if reviewer_res.get("status") == "approved":
                break

            # If rejected and retries remain, loop back
            if reviewer_res.get("status") == "rejected" and retries < 2:
                feedback = reviewer_res.get("specific_feedback", "Rewrite is needed.")
                retries += 1
            else:
                break

        # Finalizing pipeline outcome
        if reviewer_res.get("status") == "approved":
            job.status = "done"
            job.progress_message = "Generation pipeline completed successfully!"
            job.completed_at = get_utc_now()
            
            # Save the final post draft
            post = Post(
                user_id=user_uuid,
                agent_job_id=job_uuid,
                content=writer_res.get("post_content"),
                hook=writer_res.get("hook"),
                topic=research_res.get("recommended_topic"),
                content_pillar=research_res.get("content_pillar"),
                quality_score=reviewer_res.get("quality_score", 85),
                status="draft"
            )
            db.add(post)
            await db.commit()
            return

        else:
            # Rejection with retry limit exceeded -> Hard failed
            job.status = "failed"
            job.progress_message = "Reviewer Agent rejected the post after max retries."
            job.error = "MAX_RETRIES_REACHED"
            job.completed_at = get_utc_now()
            
            # save_draft_anyway
            post = Post(
                user_id=user_uuid,
                agent_job_id=job_uuid,
                content=writer_res.get("post_content") if writer_res else "Failed draft content.",
                hook=writer_res.get("hook") if writer_res else "Failed hook.",
                topic=research_res.get("recommended_topic") if research_res else "Failed topic.",
                content_pillar=research_res.get("content_pillar") if research_res else "general",
                quality_score=reviewer_res.get("quality_score", 50),
                status="draft"
            )
            db.add(post)
            await db.commit()
            return

    except Exception as e:
        job.status = "failed"
        job.progress_message = f"Orchestrator encountered error: {str(e)}"
        job.error = str(e)
        job.completed_at = get_utc_now()
        await db.commit()
        return
