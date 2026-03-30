from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.qdrant import init_qdrant
from app.api import upload, search, chat

app = FastAPI(title="AI-Qdrant-Fullstack")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], # Allow your React app
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    init_qdrant()

app.include_router(upload.router, prefix="/api")
app.include_router(search.router, prefix="/api")
app.include_router(chat.router, prefix="/api")

@app.get("/")
def health():
    return {"status": "online"}
