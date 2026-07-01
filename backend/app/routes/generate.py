# backend/app/routes/generate.py
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import Literal

from app.database import get_db
from app.models.user import User
from app.models.persona import Persona
from app.models.post import Post
from app.models.agent_job import AgentJob
from app.routes.auth import require_auth
from app.services.rate_limiter import check_generation_limit, decrement_generation_count
from app.services.qdrant_client import get_client, COLLECTION
from qdrant_client.models import Filter, FieldCondition, MatchValue
from app.tasks.pipeline import run_generation_pipeline
from app.utils.envelope import EnvelopedRoute

router = APIRouter(prefix="/generate", tags=["generate"], route_class=EnvelopedRoute)

class GenerateRequest(BaseModel):
    trigger: Literal["manual", "scheduled"] = "manual"

@router.post("", status_code=202)
async def generate_post(
    body: GenerateRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_auth)
):
    """
    POST /generate
    Starts async agent pipeline.
    """
    user_id_str = str(user.id)
    
    # 1. Check Rate Limit
    allowed, remaining = await check_generation_limit(user_id_str)
    if not allowed:
        raise HTTPException(
            status_code=429,
            detail={"code": "RATE_LIMIT_EXCEEDED", "message": "Daily generation quota (10/day) exceeded."}
        )

    # 2. Check Persona
    result = await db.execute(select(Persona).where(Persona.user_id == user.id))
    persona = result.scalar_one_or_none()
    if not persona:
        await decrement_generation_count(user_id_str)
        raise HTTPException(
            status_code=404,
            detail={"code": "PERSONA_NOT_FOUND", "message": "Persona setup missing. Please set up your creator persona."}
        )

    # 3. Check Qdrant voice memory (min 3 posts)
    try:
        client = get_client()
        count_res = client.count(
            collection_name=COLLECTION,
            count_filter=Filter(
                must=[
                    FieldCondition(key="user_id", match=MatchValue(value=user_id_str)),
                    FieldCondition(key="type", match=MatchValue(value="past_post"))
                ]
            )
        )
        post_count = count_res.count
    except Exception:
        post_count = 0

    if post_count < 3:
        await decrement_generation_count(user_id_str)
        raise HTTPException(
            status_code=400,
            detail={"code": "VOICE_MEMORY_EMPTY", "message": f"Voice memory requires at least 3 past posts. Currently indexed: {post_count}."}
        )

    # 4. Create Agent Job
    job = AgentJob(
        user_id=user.id,
        status="pending",
        progress_message="Job queued. Preparing agents..."
    )
    db.add(job)
    await db.commit()
    await db.refresh(job)

    # 5. Dispatch background task
    run_generation_pipeline.delay(user_id_str, str(job.id))

    return {"job_id": str(job.id), "status": "pending"}

@router.get("/{job_id}")
async def get_generation_status(
    job_id: str,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_auth)
):
    """
    GET /generate/{job_id}
    Polls active job status and progress.
    """
    try:
        job_uuid = uuid.UUID(job_id)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail={"code": "INVALID_JOB_ID", "message": "Invalid job ID format"}
        )

    result = await db.execute(
        select(AgentJob).where((AgentJob.id == job_uuid) & (AgentJob.user_id == user.id))
    )
    job = result.scalar_one_or_none()
    if not job:
        raise HTTPException(
            status_code=404,
            detail={"code": "JOB_NOT_FOUND", "message": "Agent job not found"}
        )

    # If job completed, query the post table to find the linked post id
    post_id = None
    if job.status in ("done", "failed"):
        post_res = await db.execute(
            select(Post.id).where((Post.agent_job_id == job_uuid) & (Post.user_id == user.id))
        )
        post_row = post_res.scalar_one_or_none()
        if post_row:
            post_id = str(post_row)

    return {
        "job_id": str(job.id),
        "status": job.status,
        "progress_message": job.progress_message,
        "post_id": post_id,
        "error": job.error
    }
