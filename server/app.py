from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from qa_pipeline import load_documents, embed_documents, find_answer

app = FastAPI()


# enable CORS for frontend-backend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

# load and embed documents on startup
# this avoids reloading and embedding the documents on every request
documents = load_documents("documents") 
doc_embeddings = embed_documents(documents)  

# define the data model for API requests
class Question(BaseModel):
    query: str  

# API endpoint: handles user questions and returns answer, source, and confidence score
@app.post("/ask")
async def ask_question(question: Question):
    """
    Handles user queries, retrieves the most relevant document,
    and generates a conversational answer with source citation and confidence score.
    """
    # use find_answer function to get the structured response
    result = find_answer(question.query, documents, doc_embeddings, top_n=2)

    # return the structured response as a JSON object
    return {
        "answer": result["answer"],        
        "source": result["source"],       
        "confidence": result["confidence"]
    }

# root endpoint
@app.get("/")
async def root():
    return {"message": "This is the RAG QA backend."}

