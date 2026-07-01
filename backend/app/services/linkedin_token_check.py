# backend/app/services/linkedin_token_check.py
from app.models.user import User
from app.database import get_utc_now

class LinkedInTokenExpired(Exception):
    pass

class LinkedInNotConnected(Exception):
    pass

def check_linkedin_token_valid(user: User, warn_days: int = 7) -> dict:
    if not user.linkedin_access_token or not user.linkedin_token_expiry:
        raise LinkedInNotConnected("User has not connected LinkedIn")

    now = get_utc_now()
    if user.linkedin_token_expiry <= now:
        raise LinkedInTokenExpired("LinkedIn token has expired — reconnect required")

    days_remaining = (user.linkedin_token_expiry - now).days
    return {
        "valid": True,
        "expiring_soon": days_remaining <= warn_days,
        "days_remaining": days_remaining
    }
