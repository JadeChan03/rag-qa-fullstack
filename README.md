# RAG QA Fullstack

A full-stack Question-Answering (QA) system that uses Retrieval-Augmented Generation (RAG) to provide accurate, contextually relevant answers from unstructured documents.

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

### Trade-offs/Limitations

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
- **Hugging Face Transformers**: For leveraging the `google/flan-t5-large` model to generate answers.
- **Python**: Core programming language for backend development.
- **Node.js**: For managing frontend dependencies and running the development server.
- **React (Vite/TypeScript)**: For building a fast, interactive and type-safe frontend.
- **Material-UI (MUI)**: For creating a consistent and responsive frontend design.
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

3. **Set the Python Version Using pyenv**  
   If you use `pyenv` to manage Python versions, you can set the local Python version for the project.

   1. In the `/server` directory, set the local Python version:
      ```bash
      pyenv local 3.10.0
      ```

   2. Verify the Python version:
      ```bash
      pyenv version
      ```

   Ensure the output matches the required version (e.g., `3.10.0`).

   If you don’t have `pyenv` installed, you can follow the [pyenv installation guide](https://github.com/pyenv/pyenv#installation).

4. **Create and Activate the Virtual Environment**    
   To isolate dependencies and avoid conflicts, create a virtual environment.
   
   ***On macOS/Linux:***
   ```bash
   python3 -m venv venv
   source venv/bin/activate 
   ```
   ***On Windows:***
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

5. **Install Dependencies**
   Once the virtual environment is activated, install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

6. **Select the Correct Python Interpreter in Visual Studio Code** 
   To avoid dependency import errors, ensure that VS Code is using the correct Python interpreter:
   - Press `Cmd+Shift+P` (macOS) or `Ctrl+Shift+P` (Windows/Linux).
   - Search for and select **Python: Select Interpreter**.
   - Choose the interpreter located in the `venv` folder. For example, `server/venv/bin/python` or `server/venv/Scripts/python.exe`.

7. **Start the Backend Server**
   ```bash
   uvicorn app:app --reload
   ```
   
   Access the backend at `http://127.0.0.1:8000` or `http://127.0.0.1:8000/docs`.

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

   Access the frontend at `http://localhost:5173`.

---

## How to Use

1. **Activate your Virtual Environment and Select the Correct Python Interpreter**
   - Ensure the correct virtual environment (`source venv/bin/activate` or `.\venv\Scripts\activate`) and Python Interpreter are selected. 
3. **Start the Backend**:
   - Ensure the backend server is running (`uvicorn app:app --reload`).

4. **Start the Frontend**:
   - Ensure the frontend is running ('`npm run dev`). Open your browser and visit `http://localhost:5173`.

5. **Ask a Question**:
   - Type your question into the input field and click "Submit."
   - The system will process the query and retrieve an answer from the documents.

---

### Alternate Usage with Only the Backend

1. **Start the Backend**:
   - Run the backend server:
     ```bash
     uvicorn app:app --reload
     ```

2. **Interact with the API**:
   - **Using Swagger UI**:
     - Open your browser and navigate to `http://127.0.0.1:8000/docs`.
     - Use the interactive Swagger UI to test the `/query` endpoint by entering your query and viewing the response.
   - **Using Postman or cURL**:
     - Send a POST request to the `/query` endpoint.
     - Example using `curl`:
       ```bash
       curl -X POST "http://127.0.0.1:8000/query" \
       -H "Content-Type: application/json" \
       -d '{"query": "What is the purpose of this project?"}'
       ```

---

## Sample Questions to Ask the Q&A System 
These questions are based on the sample client documents.

Document: HR_Remote_Work_Policy.txt

1. "Who is eligible for remote work under the updated policy?"
2. "What are the standard work hours for remote employees, and are flexible arrangements allowed?"

Document: Internal_Announcement_Q3Goals.txt

1. "When is Project Phoenix (Customer Portal Upgrade) scheduled to launch?"
2. "What is the deadline for completing cybersecurity training for all staff?"

Document: Product_Spec.txt

1. "What new features are introduced in Widget Alpha v2.1?"
2. "What is the average processing latency and throughput capacity of Widget Alpha v2.1?"

Document: Project_Summary.txt

1. "What is the primary goal of Project Phoenix?"
2. "What are the identified risks that could impact the completion of Project Phoenix?"

***Known Errors Due to Wording***
Some questions provide inaccurate or incomplete response due to wording. To improve accuracy, simplifying questions and/or rewording them into direct requests may help.

- "Who is working on Project Phoenix?"
Answer: John Smith * Tech Lead: Alice Green
- "Name everyone on Project Phoenix"
Answer: "Jane Doe (VP, Customer Success) * Project Manager: John Smith * Tech Lead: Alice Green * Primary Users: Customer Support Team, End Customers"

- "What are the remote work policy?"
Answer: All remote work must comply with the company's data security and confidentiality policies
- "Summarise the remote work policy"
Answer: **1. Security:** All remote work must comply with the company's data security and confidentiality policies. Eligibility:** Full-time employees with manager approval and a role suitable for remote work are eligible. Communication:** Remote employees are expected to be reachable via company-approved communication channels (Slack, Email, Video Conferencing) during work hours.

- "What is the deadline for completing mandatory cybersecurity training for all staff?"
Answer: August 1, 2024 (Incorrect)
- "What is the deadline for completing cybersecurity training for all staff?"
Answer: September 30th (Correct)

- "What are the key initiatives planned to enhance customer retention in Q3 2025?"
Answer: Let's work together to make Q3 a successful quarter (Irrelevant)
- "How will customer retention be improved?"
Answer: Reduce average support ticket resolution time by 15% (Better but still incomplete)

---

## Future Improvements (on RAG system)
1. **Scalability**:
   - Implement a vector database like **Pinecone**, **Weaviate**, or **FAISS** for storing document embeddings.
2. **Support for More Document Types**:
   - Add preprocessing pipelines to handle PDFs, Word documents, and other formats.
3. **Improved Answer Generation**:
   - Fine-tune a language model for domain-specific queries to improve accuracy and relevance.
4. **Improving Response Time**:
   - Utilize caching responses, further batching LLM requests, and asynchronous processing to improve pipeline efficiency.
