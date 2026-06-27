import random
import hashlib
from openai import AsyncOpenAI
from app.config import settings

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

class EmbeddingError(Exception):
    """Raised when embedding generation fails."""
    pass

async def embed_text(text: str) -> list[float]:
    """
    Embed text using OpenAI text-embedding-3-small.
    Returns a list of 1536 floats.
    Raises EmbeddingError on failure.
    """
    if not text or not text.strip():
        raise EmbeddingError("Cannot embed empty text")

    # Local mock fallback for testing without real OpenAI Key
    if not settings.OPENAI_API_KEY or settings.OPENAI_API_KEY.startswith("mock") or settings.OPENAI_API_KEY == "sk-...":
        h = hashlib.md5(text.encode("utf-8")).hexdigest()
        seed = int(h, 16) % (2**32)
        rng = random.Random(seed)
        return [rng.uniform(-1, 1) for _ in range(1536)]

    # Truncate to 8000 tokens max (approx 32000 chars)
    text = text[:32000]

    try:
        response = await client.embeddings.create(
            model="text-embedding-3-small",
            input=text.strip()
        )
        vector = response.data[0].embedding
        if len(vector) != 1536:
            raise EmbeddingError(f"Unexpected dimensions: {len(vector)}")
        return vector
    except Exception as e:
        raise EmbeddingError(f"Embedding failed: {str(e)}") from e

async def embed_batch(texts: list[str]) -> list[list[float]]:
    """Embed multiple texts in one API call (more efficient)."""
    if not texts:
        return []

    # Local mock fallback
    if not settings.OPENAI_API_KEY or settings.OPENAI_API_KEY.startswith("mock") or settings.OPENAI_API_KEY == "sk-...":
        vectors = []
        for t in texts:
            h = hashlib.md5(t.encode("utf-8")).hexdigest()
            seed = int(h, 16) % (2**32)
            rng = random.Random(seed)
            vectors.append([rng.uniform(-1, 1) for _ in range(1536)])
        return vectors

    try:
        response = await client.embeddings.create(
            model="text-embedding-3-small",
            input=[t[:32000] for t in texts]
        )
        return [item.embedding for item in response.data]
    except Exception as e:
        raise EmbeddingError(f"Batch embedding failed: {str(e)}") from e
