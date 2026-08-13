from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from services.rag import generate_rag_response
from fastapi.responses import FileResponse
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from services.rag import stream_rag_response

# initialize the FastAPI application

app = FastAPI(
    title="Cybersecurity Threat Intel RAG",
    description="An API that answers questions based on APT29 threat report"
)

# mount static directory to serve CSS and JS files
app.mount("/static", StaticFiles(directory="static"), name="static")

# define expected JSON payload structure
class QuestionRequest(BaseModel):
    query: str

@app.get("/")
def read_root():
    return FileResponse("static/index.html")

# create primary API endpoint
@app.post("/ask")
def ask_question(request: dict):
    user_query = request.get("query")

    if not user_query:
        return {"Error": "No query provided"}

    return StreamingResponse(
        stream_rag_response(user_query),
        media_type="text/event-stream"
    )