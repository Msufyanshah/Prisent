from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from app.config import settings

def get_qdrant_client() -> QdrantClient:
    return QdrantClient(
        url=settings.QDRANT_URL,
        api_key=settings.QDRANT_API_KEY or None
    )

def create_collections():
    """Run once at startup to ensure collections exist."""
    client = get_qdrant_client()

    existing = [c.name for c in client.get_collections().collections]

    if "user_voice_memory" not in existing:
        client.create_collection(
            collection_name="user_voice_memory",
            vectors_config=VectorParams(
                size=1536,                  # text-embedding-3-small dimensions
                distance=Distance.COSINE    # cosine similarity for semantic search
            )
        )
        print("Created collection: user_voice_memory")
    else:
        print("Collection already exists: user_voice_memory")
