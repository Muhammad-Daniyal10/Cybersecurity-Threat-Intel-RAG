from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from services.rag import generate_rag_response
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

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
def ask_question(request: QuestionRequest):
    try:
        print(f"\n--- New API request received ---")
        # pass incoming query to existing RAG pipeline
        answer = generate_rag_response(request.query)
        return {"answer": answer}
    except Exception as e:
        # return clean 500 error if anything in pipeline fails
        raise HTTPException(status_code=500, detail=str(e))