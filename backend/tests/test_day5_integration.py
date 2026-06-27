import sys
import os
import asyncio

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.agents.research_agent import run_research_agent
from app.agents.writer_agent import run_writer_agent
from app.agents.reviewer_agent import run_reviewer_agent
from app.services.qdrant_client import delete_user_documents

async def test_day5_integration():
    TEST_USER = "integration-test-user-005"
    await delete_user_documents(TEST_USER)

    print("Step 1: Running Research Agent...")
    research_output = await run_research_agent(
        niche="Agentic AI",
        content_pillars=["Agentic AI", "RAG Systems"],
        target_audience="Developers",
        avoid_topics=["crypto"],
        recent_post_topics=[]
    )
    print("Research Output:", research_output)

    print("\nStep 2: Feeding topic to Writer Agent...")
    persona = {
        "tone": "bold",
        "content_pillars": ["Agentic AI", "RAG Systems"],
        "content_goal": "build_authority",
        "unique_differentiator": "Deploying production agents since 2024"
    }

    writer_output = await run_writer_agent(
        user_id=TEST_USER,
        research=research_output,
        persona=persona
    )
    print("Writer Output:", writer_output)

    print("\nStep 3: Running Reviewer Agent on the draft...")
    reviewer_output = await run_reviewer_agent(
        user_id=TEST_USER,
        post_draft=writer_output,
        persona=persona,
        voice_memory_samples=["Building production agents is my focus. Naive pipelines fail."],
        retry_count=0
    )
    print("Reviewer Output:", reviewer_output)
    
    assert reviewer_output["status"] in ("approved", "rejected")
    print("\nDay 5 Integration Checkpoint: PASS")

if __name__ == "__main__":
    asyncio.run(test_day5_integration())
