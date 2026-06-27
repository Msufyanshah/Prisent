from pydantic import BaseModel
from typing import Optional

class SeedPost(BaseModel):
    content: str
    approximate_date: Optional[str] = None

class SeedPostsRequest(BaseModel):
    posts: list[SeedPost]

class SeedPostsResponse(BaseModel):
    indexed: int
    failed: int
    total_in_memory: int
