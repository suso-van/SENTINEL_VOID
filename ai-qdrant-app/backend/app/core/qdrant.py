from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from app.core.config import settings

client = QdrantClient(host=settings.QDRANT_HOST, port=settings.QDRANT_PORT)

def init_qdrant():
    try:
        collections = client.get_collections().collections
        exists = any(c.name == settings.COLLECTION_NAME for c in collections)
        
        if not exists:
            client.create_collection(
                collection_name=settings.COLLECTION_NAME,
                vectors_config=VectorParams(size=settings.VECTOR_SIZE, distance=Distance.COSINE),
            )
            print(f"✅ Qdrant Collection '{settings.COLLECTION_NAME}' Ready.")
    except Exception as e:
        print(f"❌ Qdrant Connection Error: {e}")

def get_client():
    return client