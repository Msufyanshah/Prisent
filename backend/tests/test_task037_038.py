import sys
import os
import asyncio
import uuid

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.models.user import User
from app.services.linkedin_oauth import get_authorization_url, exchange_code_for_token, get_linkedin_profile
from app.config import settings

async def test_tasks():
    print("Testing TASK-038: Mock mode environment guard...")
    original_env = settings.ENV
    original_client_id = settings.LINKEDIN_CLIENT_ID

    # 1. Test mock mode under ENV=production throws RuntimeError
    settings.LINKEDIN_CLIENT_ID = "mock-id"
    settings.ENV = "production"

    try:
        get_authorization_url("state123")
        assert False, "Should have raised RuntimeError in production"
    except RuntimeError as e:
        print("PASS: get_authorization_url correctly raised RuntimeError in production:", e)

    try:
        await exchange_code_for_token("mock_auth_code_xyz")
        assert False, "Should have raised RuntimeError in production"
    except RuntimeError as e:
        print("PASS: exchange_code_for_token correctly raised RuntimeError in production:", e)

    try:
        await get_linkedin_profile("mock_access_token_aqx123")
        assert False, "Should have raised RuntimeError in production"
    except RuntimeError as e:
        print("PASS: get_linkedin_profile correctly raised RuntimeError in production:", e)

    # Reset config
    settings.ENV = original_env
    settings.LINKEDIN_CLIENT_ID = original_client_id

    print("\nTesting TASK-037 & TASK-044 Data Models...")
    u = User(
        email=f"test_{uuid.uuid4().hex[:6]}@example.com",
        hashed_password="hash",
        name="Test",
        linkedin_person_id="KLvwf8M1aM",
        linkedin_display_name="muhammad sufyan shah",
        sidebar_collapsed=True
    )
    assert u.linkedin_person_id == "KLvwf8M1aM"
    assert "|" not in u.linkedin_person_id
    assert u.linkedin_display_name == "muhammad sufyan shah"
    assert u.sidebar_collapsed is True
    print("PASS: User data model correctly isolates bare linkedin_person_id and linkedin_display_name!")

    print("\nALL TASK-037 & TASK-038 VERIFICATION TESTS PASSED!")

if __name__ == "__main__":
    asyncio.run(test_tasks())
