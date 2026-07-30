import httpx
from app.models.user import User
from app.services.encryption import decrypt_token

LINKEDIN_SOCIAL_ACTIONS_URL = "https://api.linkedin.com/v2/socialActions/{urn}"

class LinkedInAnalyticsError(Exception):
    pass

async def fetch_post_analytics(user: User, linkedin_post_id: str) -> dict:
    """
    Fetch engagement metrics for a published post.
    Returns: {impressions, reactions, comments, reposts}

    Note: LinkedIn's Member Social Actions API provides likes/comments.
    Impressions require the Marketing Developer Platform (separate approval tier)
    not requested in TASK-019. impressions defaults to 0 — a documented MVP
    limitation, not a bug. Logged in IMPL.md Spec Compliance Tracker.
    """
    if not user.linkedin_access_token:
        raise LinkedInAnalyticsError("User does not have a linked LinkedIn account")

    access_token = decrypt_token(user.linkedin_access_token)

    async with httpx.AsyncClient() as client:
        response = await client.get(
            LINKEDIN_SOCIAL_ACTIONS_URL.format(urn=linkedin_post_id),
            headers={
                "Authorization": f"Bearer {access_token}",
                "X-Restli-Protocol-Version": "2.0.0"
            }
        )

    if response.status_code != 200:
        raise LinkedInAnalyticsError(f"LinkedIn analytics error {response.status_code}: {response.text}")

    data = response.json()
    return {
        "impressions": 0,
        "reactions": data.get("likesSummary", {}).get("totalLikes", 0),
        "comments": data.get("commentsSummary", {}).get("totalFirstLevelComments", 0),
        "reposts": 0
    }
