from fastapi import APIRouter, Query
from app.core.qdrant import get_client
from app.services.embedder import get_embeddings
from app.core.config import settings

router = APIRouter() # This MUST be here
q_client = get_client()

@router.get("/search") 
async def search_documents(q: str):
    # This turns your text into a vector
    query_vector = get_embeddings(q)
    results = q_client.search(
        collection_name=settings.COLLECTION_NAME,
        query_vector=query_vector,
        limit=5
    )
    return [{"text": r.payload["text"], "score": r.score} for r in results]

@router.get("/recommend")
async def recommend_similar(point_id: str):
    # This is for finding similar items by ID
    results = q_client.recommend(
        collection_name=settings.COLLECTION_NAME,
        positive=[point_id],
        limit=5
    )
    return results