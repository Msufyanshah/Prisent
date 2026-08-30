from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PayloadSchemaType
from app.config import settings

_cached_client = None

def _ensure_collection(client: QdrantClient):
    try:
        existing = [c.name for c in client.get_collections().collections]
        if "user_voice_memory" not in existing:
            client.create_collection(
                collection_name="user_voice_memory",
                vectors_config=VectorParams(
                    size=1536,
                    distance=Distance.COSINE
                )
            )
            print("Created collection: user_voice_memory")

        try:
            client.create_payload_index(
                collection_name="user_voice_memory",
                field_name="user_id",
                field_schema=PayloadSchemaType.KEYWORD
            )
        except Exception:
            pass

        try:
            client.create_payload_index(
                collection_name="user_voice_memory",
                field_name="type",
                field_schema=PayloadSchemaType.KEYWORD
            )
        except Exception:
            pass
    except Exception as e:
        print(f"Failed to ensure collection: {e}")

def get_qdrant_client() -> QdrantClient:
    global _cached_client
    if _cached_client is not None:
        return _cached_client

    if settings.QDRANT_URL == ":memory:":
        _cached_client = QdrantClient(":memory:")
        _ensure_collection(_cached_client)
        return _cached_client

    try:
        client = QdrantClient(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY or None,
            timeout=3.0
        )
        _ensure_collection(client)
        _cached_client = client
        return _cached_client
    except Exception as e:
        print(f"Warning: Qdrant connection to {settings.QDRANT_URL} failed ({str(e)}). Falling back to in-memory ':memory:' mode.")
        settings.QDRANT_URL = ":memory:"
        _cached_client = QdrantClient(":memory:")
        _ensure_collection(_cached_client)
        return _cached_client

def create_collections():
    """Run once at startup to ensure collections exist."""
    get_qdrant_client()


