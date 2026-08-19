import sys
import os
import asyncio

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.agents.hashtag_agent import run_hashtag_agent, append_hashtags_to_post, _to_camel_hashtag

async def test_hashtag_pipeline():
    print("Testing TASK-046: Keyword-Extraction Hashtag Pipeline...")
    
    # Test _to_camel_hashtag
    assert _to_camel_hashtag("b2b saas") == "#B2BSaas"
    assert _to_camel_hashtag("vector databases") == "#VectorDatabases"
    print("PASS: CamelCase hashtag formatting works!")

    post_text = "The future of B2B SaaS requires fundamental workflow restructuring. Vector databases and AI agents are revolutionizing execution speed."
    tags = await run_hashtag_agent(post_text, niche="Software Engineering")

    assert isinstance(tags, list)
    assert 3 <= len(tags) <= 5
    for tag in tags:
        assert tag.startswith("#")
    print(f"PASS: Generated hashtags: {tags}")

    final_post = append_hashtags_to_post(post_text, tags)
    assert tags[0] in final_post
    assert post_text in final_post
    print("PASS: Hashtags appended to post content cleanly!")

    print("ALL HASHTAG PIPELINE TESTS PASSED!")

if __name__ == "__main__":
    asyncio.run(test_hashtag_pipeline())
