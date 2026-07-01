# backend/app/services/linkedin_publisher.py
import httpx
from app.models.user import User
from app.services.encryption import decrypt_token
from app.services.linkedin_token_check import check_linkedin_token_valid
import secrets

LINKEDIN_UGC_POST_URL = "https://api.linkedin.com/v2/ugcPosts"

class LinkedInPublishError(Exception):
    pass

async def publish_to_linkedin(user: User, content: str) -> str:
    check_linkedin_token_valid(user)

    access_token = decrypt_token(user.linkedin_access_token)
    person_urn = f"urn:li:person:{user.linkedin_person_id}"

    # Handle offline mock flow
    if user.linkedin_person_id == "mock_person_id_999" or access_token == "mock_access_token_aqx123":
        return f"urn:li:share:mock_post_{secrets.token_hex(8)}"

    payload = {
        "author": person_urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": content},
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            LINKEDIN_UGC_POST_URL,
            json=payload,
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
                "X-Restli-Protocol-Version": "2.0.0"
            }
        )

    if response.status_code != 201:
        raise LinkedInPublishError(f"LinkedIn API error {response.status_code}: {response.text}")

    post_urn = response.headers.get("x-restli-id", "")
    return post_urn
