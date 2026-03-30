from fastapi import APIRouter, UploadFile, File
from qdrant_client.http.models import PointStruct
import uuid
from app.core.qdrant import get_client
from app.services.embedder import get_embeddings
from app.core.config import settings

router = APIRouter()
q_client = get_client()

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    content = await file.read()
    text = content.decode("utf-8")
    
    # Simple chunking logic
    chunks = [text[i:i+500] for i in range(0, len(text), 500)]
    points = []
    
    for chunk in chunks:
        vector = get_embeddings(chunk)
        points.append(PointStruct(
            id=str(uuid.uuid4()),
            vector=vector,
            payload={"text": chunk, "metadata": {"filename": file.filename}}
        ))
    
    q_client.upsert(collection_name=settings.COLLECTION_NAME, points=points)
    return {"status": "success", "chunks_indexed": len(chunks)}

@router.post("/upload")
async def upload_document(file: UploadFile, user_id: str): 
    # Notice the user_id! 
    # We now store vectors with a metadata tag: {"user_id": user_id}
    # This ensures Susovan only searches Susovan's files.
    
    text = await file.read()
    vector = get_embeddings(text.decode())
    
    q_client.upsert(
        collection_name="user_data",
        points=[
            PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={"text": text.decode(), "user_id": user_id} # Multi-tenant
            )
        ]
    )
    return {"status": "Vault Updated"}