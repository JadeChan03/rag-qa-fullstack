# RAG QA Fullstack

## Problem Interpretation

Many organizations struggle to efficiently retrieve precise answers from large volumes of unstructured textual data. Traditional keyword-based search methods often return irrelevant results, requiring significant manual effort to sift through them. The goal of this Proof of Concept (PoC) is to develop a **Question-Answering (QA)** system that uses **Retrieval-Augmented Generation (RAG)** to provide accurate and contextually relevant answers by leveraging a combination of document embeddings and machine learning models.

---

## Proposed Solution & Rationale

### Chosen Technical Approach
We implemented a **RAG-based QA system** that combines **document retrieval** and **text generation**:
1. **Document Processing**:
   - The backend processes and embeds textual documents into vector representations using a pre-trained embedding model.
   - These embeddings are stored and used to retrieve the most contextually relevant sections of text for a given query.

2. **Answer Generation**:
   - Given a user query, the system retrieves relevant document sections and uses a language model to generate a concise answer.

3. **Frontend-Backend Integration**:
   - A **FastAPI** backend handles the document embedding, retrieval, and query processing.
   - A **React** frontend allows users to interact with the system by typing questions and receiving answers.

### Why This Approach?
- **Accuracy & Relevance**: Vector embeddings capture semantic meaning, allowing the system to retrieve and rank the most relevant documents even when queries are phrased differently.
- **Flexibility**: The architecture can be adapted to various document types and expanded with new embedding or language models.
- **User Experience**: A simple frontend ensures that even non-technical users can interact with the system effectively.

### Tools/Libraries:
- **FastAPI**: For a lightweight and performant backend.
- **Sentence Transformers**: For generating document embeddings.
- **React (Vite)**: For building a fast and interactive frontend.
- **Material-UI (MUI)**: For consistent and responsive frontend design.

#### Trade-offs:
- **Embedding Model Size**: Using larger embedding models improves accuracy but increases memory and processing time.
- **Answer Generation Quality**: While RAG outperforms traditional search, it depends on the quality of retrieved documents and the language model.
- **Scalability**: The current PoC uses an in-memory approach, which may not scale for large datasets.

---

## Setup Instructions

### Backend Setup
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/JadeChan03/rag-qa-fullstack.git
   cd rag-qa-fullstack/server
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the Backend Server**:
   ```bash
   uvicorn app:app --reload
   ```

- Access the backend at `http://127.0.0.1:8000`.

### Frontend Setup
1. **Navigate to the Client Directory**:
   ```bash
   cd ../client
   ```

2. **Install Dependencies**:
   ```bash
   npm install
   ```

3. **Start the Frontend Development Server**:
   ```bash
   npm run dev
   ```

- Access the frontend at `http://localhost:5173`.

---

## How to Use

1. **Start the Backend**:
   - Ensure the backend server is running (`uvicorn app:app --reload`).

2. **Start the Frontend**:
   - Open your browser and visit `http://localhost:5173`.

3. **Ask a Question**:
   - Type your question into the input field and click "Submit."
   - The system will process the query and retrieve an answer from the documents.

---

## Limitations & Next Steps

### Limitations
1. **Scalability**:
   - The current implementation uses in-memory storage for document embeddings, which may not scale for large datasets.
   - Running the PoC on resource-constrained environments may lead to performance bottlenecks.

2. **Document Types**:
   - The PoC currently supports plain text documents. It does not process PDFs, Word files, or other formats.

3. **Answer Quality**:
   - The quality of the generated answers depends on the relevance of the retrieved documents and the language model's capabilities.

4. **Frontend Design**:
   - The frontend is minimal and may require additional enhancements for production use.

### Next Steps
1. **Scalability**:
   - Implement a vector database like **Pinecone**, **Weaviate**, or **FAISS** for storing document embeddings.

2. **Support for More Document Types**:
   - Add preprocessing pipelines to handle PDFs, Word documents, and other formats.

3. **Improved Answer Generation**:
   - Fine-tune a language model for domain-specific queries to improve accuracy and relevance.

4. **Authentication & Authorization**:
   - Add user authentication to restrict access and provide personalized results.

5. **Deployment**:
   - Package the backend and frontend for deployment on platforms like **AWS**, **Azure**, or **Vercel**.