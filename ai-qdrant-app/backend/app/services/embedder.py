from sentence_transformers import SentenceTransformer

# This will download the model the first time you run it
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embeddings(text: str):
    return model.encode(text).tolist()