from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from qa_pipeline import load_documents, embed_documents, find_answer

# Initialize FastAPI app
app = FastAPI()

# Enable CORS for frontend-backend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with specific frontend URLs in production
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Load and embed documents on startup
# This avoids reloading and embedding the documents on every request
documents = load_documents("documents")  # Load all .txt files from the 'documents/' directory
doc_embeddings = embed_documents(documents)  # Generate embeddings for all documents

# Define the data model for API requests
class Question(BaseModel):
    query: str  # The user-provided question in natural language

# API endpoint: Handles user questions and returns answer, source, and confidence score
@app.post("/ask")
async def ask_question(question: Question):
    """
    Handles user queries, retrieves the most relevant document,
    and generates a conversational answer with source citation and confidence score.
    """
    # Use find_answer function to get the structured response
    result = find_answer(question.query, documents, doc_embeddings)

    # Return the structured response as a JSON object
    return {
        "answer": result["answer"],        # Conversational answer
        "source": result["source"],        # Source document name
        "confidence": result["confidence"] # Confidence score
    }

# Root endpoint
@app.get("/")
async def root():
    return {"message": "This is the RAG QA backend."}