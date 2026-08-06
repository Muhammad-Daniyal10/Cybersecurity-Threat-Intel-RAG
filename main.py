from fastapi import FastAPI

app = FastAPI(
    title="RAG API",
    description="A Retrieval-Augmented Generation backend",
    version="1.0.0"
)

@app.get("/")
async def health_check():
    return {
        "status": "success",
        "message": "The RAG API is running"
    }