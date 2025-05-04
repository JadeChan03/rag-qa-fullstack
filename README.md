# RAG QA Fullstack

## Problem Interpretation

Many organizations struggle to efficiently retrieve precise answers from large volumes of unstructured textual data. Traditional keyword-based search methods often return irrelevant results, requiring significant manual effort to sift through them. The goal of this Proof of Concept (PoC) is to develop a **Question-Answering (QA)** system that uses **Retrieval-Augmented Generation (RAG)** to provide accurate and contextually relevant answers by leveraging a combination of document embeddings and machine learning models.

---

## Proposed Solution & Rationale

### Chosen Technical Approach

This project implements a **Retrieval-Augmented Generation (RAG)** pipeline to answer user queries by combining document retrieval and language model-based answer generation:

1. **Document Embedding and Retrieval**:
   - Documents are loaded from a directory and converted into vector embeddings using the `all-MiniLM-L6-v2` model from **Sentence Transformers**.
   - Cosine similarity is used to compare the query embedding with document embeddings, retrieving the most relevant documents.

2. **Answer Generation**:
   - The top relevant documents are combined into a context, which is truncated to fit within a token limit.
   - The context and query are passed to the `google/flan-t5-large` model from **Hugging Face Transformers** to generate a detailed and contextually relevant answer.

3. **Confidence and Source Tracking**:
   - The system calculates confidence scores based on cosine similarity and provides the sources of the retrieved documents alongside the generated answer.

4. **Frontend-Backend Integration**:
   - A **FastAPI** backend handles document embedding, retrieval, and query processing.
   - A **React** frontend allows users to input questions and view answers in an intuitive interface.

---

### Why This Approach?

- **Semantic Understanding**: By leveraging **Sentence Transformers**, the system captures the semantic meaning of text, enabling accurate retrieval of relevant documents even for complex or rephrased queries.
- **High-Quality Answer Generation**: The `google/flan-t5-large` model generates detailed and contextually relevant answers, ensuring a high-quality user experience.
- **Explainability**: The system provides the sources of retrieved documents, enhancing transparency and trust in the generated answers.
- **Modularity**: The architecture separates document retrieval and answer generation, making it easy to upgrade or replace components (e.g., embedding models or language models).
- **Scalability**: The use of cosine similarity and embeddings allows the system to handle a variety of document types and queries efficiently.

---

### Trade-offs

- **Embedding Model Size**: The `all-MiniLM-L6-v2` model is lightweight and fast but may sacrifice some accuracy compared to larger embedding models.
- **Answer Generation Quality**: The quality of the generated answers depends on the relevance of the retrieved documents and the capabilities of the `google/flan-t5-large` model.
- **In-Memory Storage**: Document embeddings are stored in memory, which limits scalability for large datasets. A vector database like **FAISS** or **Pinecone** could be integrated for larger-scale use cases.
- **Response Time**: The pipeline's response time may be affected by the efficiency of the retrieval mechanism and the processing speed of the language model.
- **Context Truncation**: To fit within token limits, the context is truncated, which may result in the omission of some relevant details from the documents.
- **Document Format Support**: The system currently supports plain text files only, limiting its applicability to other formats like PDFs or Word documents.

---

### Tools/Libraries:
- **FastAPI**: For building a lightweight, high-performance backend API.
- **Uvicorn**: ASGI server for running the FastAPI backend.
- **Sentence Transformers**: For generating high-quality document embeddings.
- **FAISS**: For efficient similarity search and clustering of embeddings.
- **Hugging Face Transformers**: For leveraging the `google/flan-t5-large` model to generate answers.
- **React (Vite)**: For building a fast and interactive frontend.
- **Material-UI (MUI)**: For creating a consistent and responsive frontend design.
- **Python**: Core programming language for backend development.
- **Node.js**: For managing frontend dependencies and running the development server.
- **npm**: For managing JavaScript packages and scripts.

---

## Setup Instructions

**1. Clone the Repository**
   ```bash
   git clone https://github.com/JadeChan03/rag-qa-fullstack.git
   ```

### Backend Setup

2. **Navigate to the Server Directory** 
   ```bash
   cd rag-qa-fullstack/server 
   ```

3. **Create and Activate the Virtual Environment**    
   To isolate dependencies and avoid conflicts, create a virtual environment.
   On macOS/Linux:
   ```bash
   python3 -m venv venv
   source venv/bin/activate 
   ```
   On Windows:
   ```bash
   python -m venv venv
   .venv\Scripts\activate
   ```

3. **Install Dependencies**
   Once the virtual environment is activated, install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. **Select the Correct Python Interpreter in Visual Studio Code/your IDE** 
   To avoid dependency import errors, ensure that VS Code is using the correct Python interpreter:

   1. Navigate or ensure that you are in the `server` folder.
   2. Press `Cmd+Shift+P` on macOS or `Ctrl+Shift+P` on Windows/Linux.
   3. Search for and select **Python: Select Interpreter**.
   4. Choose the interpreter located in the `venv` folder. For example, `server/venv/bin/python` or `server/venv/Scripts/python.exe`.

5. **Start the Backend Server**
   ```bash
   uvicorn app:app --reload
   ```

- Access the backend at `http://127.0.0.1:8000` or `http://127.0.0.1:8000/docs`.

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

4. **Optimization for Response Time**:
   - Currently the system is operating at a relatively inefficient speed, possible due to LLM Response Time and pipeline inefficiency. 

### Next Steps
1. **Scalability**:
   - Implement a vector database like **Pinecone**, **Weaviate**, or **FAISS** for storing document embeddings.

2. **Support for More Document Types**:
   - Add preprocessing pipelines to handle PDFs, Word documents, and other formats.

3. **Improved Answer Generation**:
   - Fine-tune a language model for domain-specific queries to improve accuracy and relevance.

4. **Authentication & Authorization**:
   - Add user authentication to restrict access and provide personalized results.

5. **Improving Response Time**:
   - Utilize caching responses, further batching LLM requests, and asynchronous processing to improve pipeline efficiency.