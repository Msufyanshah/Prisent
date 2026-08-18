import sys
import os
import asyncio
import uuid
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.models.user import User
from app.models.post import Post
from app.routes.posts import update_post
from app.schemas.post import UpdatePostRequest
from app.database import AsyncSessionLocal

async def test_post_edit():
    print("Testing TASK-047: PATCH /posts/{post_id}...")
    async with AsyncSessionLocal() as db:
        user = User(
            email=f"edit_test_{uuid.uuid4().hex[:6]}@example.com",
            hashed_password="hash",
            name="Edit Tester"
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)

        post = Post(
            user_id=user.id,
            content="Original Post Content Line 1\nSecond Line of post",
            hook="Original Post Content Line 1",
            status="draft"
        )
        db.add(post)
        await db.commit()
        await db.refresh(post)

        # Execute edit request
        req = UpdatePostRequest(content="Updated Post Content Here!\nWith a brand new body paragraph.")
        updated = await update_post(str(post.id), req, current_user=user, db=db)

        assert updated.content == "Updated Post Content Here!\nWith a brand new body paragraph."
        assert updated.hook == "Updated Post Content Here!"
        print("PASS: Post content and hook updated successfully!")

        # Verify editing a published post fails
        updated.status = "published"
        await db.commit()

        try:
            from fastapi import HTTPException
            await update_post(str(post.id), req, current_user=user, db=db)
            assert False, "Should have raised HTTPException when editing published post"
        except HTTPException as e:
            assert e.status_code == 400
            print("PASS: Editing published post correctly rejected with HTTP 400!")

    print("ALL TASK-047 POST EDITING TESTS PASSED!")

if __name__ == "__main__":
    asyncio.run(test_post_edit())
