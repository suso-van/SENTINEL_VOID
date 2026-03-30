from fastapi import APIRouter
from app.core.qdrant import get_client
from app.services.embedder import get_embeddings
from app.core.config import settings

router = APIRouter()
q_client = get_client()

@router.post("/chat")
async def rag_chat(message: str):
    # 1. Retrieve Context
    vector = get_embeddings(message)
    search_results = q_client.search(
        collection_name=settings.COLLECTION_NAME,
        query_vector=vector,
        limit=3
    )
    
    context = "\n".join([r.payload["text"] for r in search_results])
    
    # 2. Construct Prompt for LLM
    prompt = f"Context: {context}\n\nUser Question: {message}\nAnswer based on context:"
    
    # Note: Integrate your LLM call (OpenAI/Groq/Ollama) here using 'prompt'
    return {"answer": "LLM integration pending", "context_used": context}