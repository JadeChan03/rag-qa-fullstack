from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from qa_pipeline import load_documents, embed_documents, find_answer

# initialize FastAPI app
app = FastAPI()

# enable CORS for frontend-backend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # replace "*" with specific frontend URLs in production
    allow_credentials=True,
    allow_methods=["*"],  # allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # allow all headers
)

# load and embed documents on startup
# this avoids reloading and embedding the documents on every request
documents = load_documents("documents")  # load all .txt files from the 'documents/' directory
doc_embeddings = embed_documents(documents)  # generate embeddings for all documents

# define the data model for API requests
class Question(BaseModel):
    query: str  # the user-provided question in natural language

# API endpoint, handles user questions and returns most relevant answer
# input: user question (JSON)
# output: dictionary containing generated answer (dict)
@app.post("/ask")
async def ask_question(question: Question):
    # use find_answer function to get the most relevant document
    answer = find_answer(question.query, documents, doc_embeddings)
    # return the answer as a JSON response
    return {"answer": answer}

# Root endpoint
@app.get("/")
async def root():
    return {"message": "This is the RAG QA Bot (fullstack) backend."}