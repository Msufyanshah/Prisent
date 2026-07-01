# backend/app/services/linkedin_oauth.py
import httpx
from app.config import settings

LINKEDIN_AUTH_URL = "https://www.linkedin.com/oauth/v2/authorization"
LINKEDIN_TOKEN_URL = "https://www.linkedin.com/oauth/v2/accessToken"
LINKEDIN_USERINFO_URL = "https://api.linkedin.com/v2/userinfo"

SCOPES = ["openid", "profile", "w_member_social"]

def get_authorization_url(state: str) -> str:
    if settings.LINKEDIN_CLIENT_ID == "mock-id":
        return f"{settings.LINKEDIN_REDIRECT_URI}?code=mock_auth_code_xyz&state={state}"

    params = {
        "response_type": "code",
        "client_id": settings.LINKEDIN_CLIENT_ID,
        "redirect_uri": settings.LINKEDIN_REDIRECT_URI,
        "state": state,
        "scope": " ".join(SCOPES)
    }
    query = "&".join(f"{k}={v}" for k, v in params.items())
    return f"{LINKEDIN_AUTH_URL}?{query}"

async def exchange_code_for_token(code: str) -> dict:
    if settings.LINKEDIN_CLIENT_ID == "mock-id" or code == "mock_auth_code_xyz":
        return {
            "access_token": "mock_access_token_aqx123",
            "expires_in": 5184000
        }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            LINKEDIN_TOKEN_URL,
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": settings.LINKEDIN_REDIRECT_URI,
                "client_id": settings.LINKEDIN_CLIENT_ID,
                "client_secret": settings.LINKEDIN_CLIENT_SECRET,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        response.raise_for_status()
        return response.json()

async def get_linkedin_profile(access_token: str) -> dict:
    if settings.LINKEDIN_CLIENT_ID == "mock-id" or access_token == "mock_access_token_aqx123":
        return {
            "sub": "mock_person_id_999",
            "name": "LinkedIn Mock User",
            "given_name": "LinkedIn Mock",
            "family_name": "User",
            "picture": "http://localhost:3000/placeholder.png",
            "email": "mock@linkedin.com"
        }

    async with httpx.AsyncClient() as client:
        response = await client.get(
            LINKEDIN_USERINFO_URL,
            headers={"Authorization": f"Bearer {access_token}"}
        )
        response.raise_for_status()
        return response.json()
