# backend/app/tasks/pipeline.py
import asyncio
from app.tasks.celery_app import celery_app
from app.database import AsyncSessionLocal
from app.agents.orchestrator import run_orchestrator

@celery_app.task(name="app.tasks.pipeline.run_generation_pipeline")
def run_generation_pipeline(user_id: str, job_id: str):
    """
    Celery background task wrapper for the agent orchestrator.
    """
    async def _execute():
        async with AsyncSessionLocal() as db:
            await run_orchestrator(user_id=user_id, job_id=job_id, db=db)

    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    if loop.is_running():
        future = asyncio.run_coroutine_threadsafe(_execute(), loop)
        future.result()
    else:
        loop.run_until_complete(_execute())
