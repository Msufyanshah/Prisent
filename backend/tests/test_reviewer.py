import sys
import os
import asyncio

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.agents.reviewer_agent import run_reviewer_agent

async def test_reviewer_agent():
    TEST_USER = 'test-reviewer-user-001'
    persona = {
        "tone": "bold",
        "content_pillars": ["Agentic AI", "RAG"]
    }
    voice_samples = [
        "Building autonomous AI agents requires a solid planning and tooling structure. Naive RAG is dead."
    ]

    # Test 1: Conforming draft is approved
    print("Testing Test 1: Conforming draft...")
    good_draft = {
        "post_content": (
            "Hook: Building production AI agents is hard.\n\n"
            "Most teams fail because they expect naive pipelines to just work. "
            "But prompt engineering is not software engineering. "
            "We spent the last 3 months deploying complex systems in production. "
            "During this period, we learned that semantic search and naive chunking are dead. "
            "You need a structured planning loop and deterministic guardrails. "
            "Additionally, tool calling must have exponential backoff and error recovery. "
            "If you do not build these mechanisms, your agents will behave unpredictably. "
            "To succeed, treat your prompts exactly like codebase versioning. "
            "Ensure you write unit tests for every tool loop and monitor LLM token costs carefully. "
            "It takes time, but this is the only way to build reliable enterprise-grade systems.\n\n"
            "What is the biggest challenge you have faced when deploying AI systems to production?"
        ),
        "hook": "Building production AI agents is hard.",
        "word_count": 140,
        "content_pillar": "Agentic AI"
    }
    res = await run_reviewer_agent(TEST_USER, good_draft, persona, voice_samples, retry_count=0)
    print("Good draft response:", res)
    assert res["status"] == "approved"
    assert res["quality_score"] >= 70
    assert "scores" in res
    print("Test 1 PASS: conforming draft approved")

    # Test 2: Draft with banned phrase is rejected
    print("\nTesting Test 2: Banned phrase draft...")
    bad_draft_banned = {
        "post_content": "Hook: Building production AI agents is hard.\n\nThoughts? What do you think about this? Comment below!",
        "hook": "Building production AI agents is hard.",
        "word_count": 15,
        "content_pillar": "Agentic AI"
    }
    res = await run_reviewer_agent(TEST_USER, bad_draft_banned, persona, voice_samples, retry_count=0)
    print("Banned phrase draft response:", res)
    assert res["status"] == "rejected"
    assert res["quality_score"] < 70
    assert any("banned" in reason for reason in res["rejection_reasons"])
    print("Test 2 PASS: banned phrase draft rejected")

    # Test 3: Draft with long hook is rejected
    print("\nTesting Test 3: Long hook draft...")
    bad_draft_hook = {
        "post_content": "Hook: This hook is definitely way too long and violates the 49 character threshold.\n\nSome body text here.",
        "hook": "This hook is definitely way too long and violates the 49 character threshold.",
        "word_count": 20,
        "content_pillar": "Agentic AI"
    }
    res = await run_reviewer_agent(TEST_USER, bad_draft_hook, persona, voice_samples, retry_count=0)
    print("Long hook response:", res)
    assert res["status"] == "rejected"
    assert any("Hook is too long" in reason for reason in res["rejection_reasons"])
    print("Test 3 PASS: long hook draft rejected")

    # Test 4: Hard fail when max retries reached
    print("\nTesting Test 4: Max retries hard fail...")
    res = await run_reviewer_agent(TEST_USER, bad_draft_banned, persona, voice_samples, retry_count=2)
    print("Max retries response:", res)
    assert res["status"] == "hard_failed"
    assert "last_draft" in res
    print("Test 4 PASS: max retries hard failed correctly")

    print("\nALL REVIEWER AGENT TESTS PASSED!")

if __name__ == "__main__":
    asyncio.run(test_reviewer_agent())
