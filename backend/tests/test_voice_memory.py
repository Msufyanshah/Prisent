import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.qdrant_setup import get_qdrant_client
from app.services.embeddings import embed_text, EmbeddingError
from app.services.qdrant_client import (
    upsert_document, retrieve_voice_memory,
    count_user_documents, delete_user_documents
)
import asyncio

def test_qdrant_collection():
    client = get_qdrant_client()
    collections = [c.name for c in client.get_collections().collections]
    assert 'user_voice_memory' in collections, 'Collection not found!'
    info = client.get_collection('user_voice_memory')
    assert info.config.params.vectors.size == 1536, 'Wrong dimensions!'
    print('Collection OK — dimensions:', info.config.params.vectors.size)
    print('Distance:', info.config.params.vectors.distance)

async def test_embeddings():
    # Test 1: Normal text returns 1536 floats
    vector = await embed_text('I build AI agents that solve real problems')
    assert len(vector) == 1536, f'Wrong length: {len(vector)}'
    assert all(isinstance(v, float) for v in vector), 'Not all floats'
    print('Test 1 PASS: vector length =', len(vector))

    # Test 2: Empty string raises EmbeddingError
    try:
        await embed_text('')
        print('Test 2 FAIL: should have raised EmbeddingError')
        assert False
    except EmbeddingError:
        print('Test 2 PASS: EmbeddingError raised correctly')

async def test_qdrant_client():
    TEST_USER = 'test-user-001'

    # Clean up any existing docs for test user
    await delete_user_documents(TEST_USER)

    # Test 1: Store a document
    doc_id = await upsert_document(
        user_id=TEST_USER,
        content='I spent 3 days debugging an AI agent. Here is what I learned about context windows and tool calling patterns.',
        doc_type='past_post',
        metadata={'pillar': 'Agentic AI', 'tone': 'storytelling'}
    )
    assert doc_id, 'No doc_id returned'
    print('Test 3 PASS: stored doc_id =', doc_id[:8], '...')

    # Test 2: Retrieve by similar topic
    results = await retrieve_voice_memory(TEST_USER, 'AI agent debugging tips', top_k=3)
    assert len(results) >= 1, 'No results returned'
    assert results[0]['content'], 'Empty content'
    print('Test 4 PASS: found', len(results), 'results, top score:', round(results[0]['relevance_score'], 3))

    # Test 3: Count documents
    count = await count_user_documents(TEST_USER)
    assert count == 1, f'Count is {count}, expected 1'
    print('Test 5 PASS: count =', count)

    # Test 4: User isolation — different user gets no results
    other_results = await retrieve_voice_memory('different-user-999', 'AI agents', top_k=5)
    assert len(other_results) == 0, 'User isolation FAILED — seeing other user data!'
    print('Test 6 PASS: user isolation confirmed')

    # Cleanup
    deleted = await delete_user_documents(TEST_USER)
    assert deleted == 1
    print('Cleanup: deleted', deleted, 'documents')

async def run_all_async():
    await test_embeddings()
    await test_qdrant_client()

import httpx

async def test_seed_posts_endpoint():
    # We must register a user, log in to get a token, and then post to /persona/seed-posts
    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        import uuid
        uid = str(uuid.uuid4())[:8]
        email = f"seed_{uid}@prisent.ai"
        
        # 1. Register
        r = await client.post("/auth/register", json={"email": email, "password": "Check1234!", "name": "Seeder"})
        assert r.status_code == 201
        token = r.json()["data"]["token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # 2. Test 1: Posting less than 3 posts fails with 400
        bad_payload = {
            "posts": [
                {"content": "Post number 1"}
            ]
        }
        r = await client.post("/persona/seed-posts", json=bad_payload, headers=headers)
        assert r.status_code == 400
        assert r.json()["error"]["code"] == "MIN_POSTS_NOT_MET"
        print("Test 7 PASS: insufficient posts rejected")

        # 3. Test 2: Posting 3 posts succeeds
        good_payload = {
            "posts": [
                {"content": "I built an autonomous pipeline today that automatically uploads files.", "approximate_date": "yesterday"},
                {"content": "AI is transforming how we write code. Highly suggest learning LLM tool calling.", "approximate_date": "1 week ago"},
                {"content": "Always verify your vector database dimensions match your embeddings.", "approximate_date": "2 weeks ago"}
            ]
        }
        r = await client.post("/persona/seed-posts", json=good_payload, headers=headers)
        assert r.status_code == 200 or r.status_code == 201
        res = r.json()
        assert res["success"] is True
        data = res["data"]
        assert data["indexed"] == 3
        assert data["failed"] == 0
        assert data["total_in_memory"] == 3
        print("Test 8 PASS: 3 posts successfully seeded and enveloped")

async def run_all_async():
    await test_embeddings()
    await test_qdrant_client()
    await test_seed_posts_endpoint()

if __name__ == "__main__":
    test_qdrant_collection()
    asyncio.run(run_all_async())
