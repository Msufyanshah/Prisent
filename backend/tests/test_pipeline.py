# backend/tests/test_pipeline.py
import sys
import os
import asyncio
import httpx
import uuid

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.qdrant_client import delete_user_documents, upsert_batch

async def run_pipeline_tests():
    print("Waiting 3 seconds for Uvicorn reloader to settle...")
    await asyncio.sleep(3)
    async with httpx.AsyncClient(base_url="http://localhost:8000", timeout=30.0) as client:
        unique_id = str(uuid.uuid4())[:8]
        email = f"pipeline_{unique_id}@prisent.ai"
        password = "Test1234!"
        
        print("1. Registering test user...")
        r = await client.post("/auth/register", json={"email": email, "password": password, "name": "Pipeline User"})
        assert r.status_code == 201
        token = r.json()["data"]["token"]
        user_id = r.json()["data"]["user_id"]
        headers = {"Authorization": f"Bearer {token}"}

        # Clean up Qdrant documents for this user
        print("Cleaning up voice memory...")
        await delete_user_documents(user_id)

        # Test A: POST /generate with NO persona -> Expect 404 PERSONA_NOT_FOUND
        print("\nTest A: Generating post without persona...")
        r = await client.post("/generate", json={"trigger": "manual"}, headers=headers)
        print("A response:", r.status_code, r.json())
        assert r.status_code == 404
        assert r.json()["error"]["code"] == "PERSONA_NOT_FOUND"
        print("Test A PASS")

        # Setup Persona
        print("\nSetting up creator persona...")
        persona_data = {
            "name": "Pipeline User",
            "headline": "Software Architect",
            "niche": "Distributed Systems",
            "content_pillars": ["Systems design", "Databases"],
            "tone": "conversational",
            "target_audience": "Senior devs",
            "content_goal": "build_authority",
            "posting_frequency": "3x_week",
            "unique_differentiator": "10 years scaling databases"
        }
        r = await client.post("/persona", json=persona_data, headers=headers)
        assert r.status_code == 200

        # Test B: POST /generate with persona but EMPTY voice memory -> Expect 400 VOICE_MEMORY_EMPTY
        print("\nTest B: Generating post without voice memory...")
        r = await client.post("/generate", json={"trigger": "manual"}, headers=headers)
        print("B response:", r.status_code, r.json())
        assert r.status_code == 400
        assert r.json()["error"]["code"] == "VOICE_MEMORY_EMPTY"
        print("Test B PASS")

        # Seed past posts (3 posts)
        print("\nSeeding 3 past posts for voice memory...")
        samples = [
            {"content": "Building reliable queues is all about handling network splits and ensuring backpressure.", "type": "past_post"},
            {"content": "When picking a database, understand your access patterns. Read-heavy vs write-heavy matters.", "type": "past_post"},
            {"content": "Alembic migrations are the backbone of schema evolution. Always write down-migration scripts.", "type": "past_post"}
        ]
        await upsert_batch(user_id, samples)

        # Test C: POST /generate -> Expect 202 and Job Queued
        print("\nTest C: Starting generation pipeline...")
        r = await client.post("/generate", json={"trigger": "manual"}, headers=headers)
        print("C response:", r.status_code, r.json())
        assert r.status_code == 202
        job_id = r.json()["data"]["job_id"]
        assert r.json()["data"]["status"] == "pending"
        print("Test C PASS")

        # Run the orchestrator directly inside the async test runner to process the pending job in DB
        print("Executing orchestrator directly...")
        from app.database import AsyncSessionLocal
        from app.agents.orchestrator import run_orchestrator
        async with AsyncSessionLocal() as db:
            await run_orchestrator(user_id, job_id, db)

        # Test D: GET /generate/{job_id} -> Expect done
        print("\nTest D: Polling generation status...")
        r = await client.get(f"/generate/{job_id}", headers=headers)
        print("D response:", r.status_code, r.json())
        assert r.status_code == 200
        data = r.json()["data"]
        assert data["status"] == "done"
        assert data["post_id"] is not None
        print("Test D PASS")

        # Clean up Qdrant documents
        await delete_user_documents(user_id)
        print("\nALL PIPELINE ASYNC TESTS PASSED!")

if __name__ == "__main__":
    asyncio.run(run_pipeline_tests())
