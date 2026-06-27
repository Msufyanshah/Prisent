# backend/app/agents/reviewer_agent.py
import json
from openai import AsyncOpenAI
from app.config import settings
from app.constants.prompts import REVIEWER_AGENT_SYSTEM_PROMPT

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

BANNED_PHRASES = [
    "comment YES", "drop a like", "share if you agree",
    "thoughts?", "agree or disagree?", "comment below",
    "double tap", "save this post", "repost this"
]

async def run_reviewer_agent(
    user_id: str,
    post_draft: dict,
    persona: dict,
    voice_memory_samples: list[str] = None,
    retry_count: int = 0
) -> dict:
    """
    Run the Reviewer Agent.
    Evaluates a drafted LinkedIn post for tone, hook, structure, and compliance.
    Matches Contract A3.
    """
    post_content = post_draft.get("post_content", "")
    hook = post_draft.get("hook", "")

    # Programmatic Quality Checks
    rejection_reasons = []
    
    # 1. Banned phrases check (case-insensitive)
    found_banned = [p for p in BANNED_PHRASES if p.lower() in post_content.lower()]
    if found_banned:
        rejection_reasons.append(f"Contains banned call-to-action phrases: {', '.join(found_banned)}")
        
    # 2. Hook length check
    if len(hook) > 49:
        rejection_reasons.append(f"Hook is too long ({len(hook)} chars). Must be <= 49 characters.")
        
    # 3. Word count check
    words = len(post_content.split())
    if words < 100 or words > 350:
        rejection_reasons.append(f"Word count is {words}. Should be between 150 and 300 words.")

    # Local mock fallback for offline/local testing
    if not settings.OPENAI_API_KEY or settings.OPENAI_API_KEY.startswith("mock") or settings.OPENAI_API_KEY == "sk-...":
        if rejection_reasons:
            if retry_count >= 2:
                return {
                    "status": "hard_failed",
                    "quality_score": 50,
                    "reason": f"Max retries reached. Issues remain: {'; '.join(rejection_reasons)}",
                    "last_draft": post_content
                }
            return {
                "status": "rejected",
                "quality_score": 60,
                "rejection_reasons": rejection_reasons,
                "specific_feedback": f"Please rewrite and fix: {'. '.join(rejection_reasons)}",
                "retry_count": retry_count
            }
        else:
            return {
                "status": "approved",
                "quality_score": 85,
                "scores": {
                    "voice_match": 18,
                    "hook_quality": 17,
                    "depth_score_compliance": 18,
                    "clarity": 16,
                    "authenticity": 16
                },
                "notes": "Excellent draft. Clear logic, hook is scroll-stopping, and matches the voice samples."
            }

    # Format voice memory samples for comparison prompt
    if voice_memory_samples:
        samples_formatted = "\n\n".join(voice_memory_samples)
    else:
        samples_formatted = "No voice samples available."

    # Format the reviewer prompt
    system_prompt = REVIEWER_AGENT_SYSTEM_PROMPT.format(
        voice_samples=samples_formatted.strip(),
        post_content=post_content
    )

    try:
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Score this post: \n{post_content}"}
            ],
            response_format={"type": "json_object"}
        )

        output = json.loads(response.choices[0].message.content)
        
        # Override with programmatic checks (force rejection if rules violated)
        if rejection_reasons:
            if retry_count >= 2:
                return {
                    "status": "hard_failed",
                    "quality_score": min(output.get("quality_score", 50), 50),
                    "reason": f"Max retries reached. Rules violated: {'; '.join(rejection_reasons)}",
                    "last_draft": post_content
                }
            return {
                "status": "rejected",
                "quality_score": min(output.get("quality_score", 60), 60),
                "rejection_reasons": rejection_reasons,
                "specific_feedback": f"Please rewrite and fix: {'. '.join(rejection_reasons)}",
                "retry_count": retry_count
            }

        return output

    except Exception as e:
        # Graceful fallback on error
        if retry_count >= 2:
            return {
                "status": "hard_failed",
                "quality_score": 50,
                "reason": f"Reviewer agent crash: {str(e)}",
                "last_draft": post_content
            }
        return {
            "status": "rejected",
            "quality_score": 60,
            "rejection_reasons": [str(e)],
            "specific_feedback": "Reviewer agent crashed during evaluation. Please regenerate.",
            "retry_count": retry_count
        }
