# RAG QA Fullstack

A full-stack Question-Answering (QA) system that uses Retrieval-Augmented Generation (RAG) to provide accurate, contextually relevant answers from unstructured documents.

---

## Table of Contents

1. [Problem Interpretation](#problem-interpretation)
2. [Proposed Solution & Rationale](#proposed-solution--rationale)
3. [Tools/Libraries](#toolslibraries)
4. [Prerequisites](#prerequisites)
5. [Quickstart](#quickstart)
6. [Setup Instructions](#setup-instructions)
7. [Troubleshooting](#troubleshooting)
8. [Questions to Ask the Q&A System](#questions-to-ask-the-qa-system)
9. [Future Improvements](#future-improvements)

---

## Problem Interpretation

Many organizations struggle to efficiently retrieve precise answers from large volumes of unstructured textual data. Traditional keyword-based search methods often return irrelevant results, requiring significant manual effort to sift through them. The goal of this Proof of Concept (PoC) is to develop a **Question-Answering (QA)** system that uses **Retrieval-Augmented Generation (RAG)** to provide accurate and contextually relevant answers by leveraging a combination of document embeddings and machine learning models.

---

## Proposed Solution & Rationale

### Chosen Technical Approach

This project implements a **Retrieval-Augmented Generation (RAG)** pipeline to answer user queries by combining document retrieval and language model-based answer generation:

1. **Document Embedding and Retrieval**:
   - Documents are loaded from a directory and converted into vector embeddings using the `all-MiniLM-L6-v2` model from **Sentence Transformers**.
   - Cosine similarity is used to compare the query embedding with document embeddings, retrieving the most relevant documents.
   - A keyword boost is applied to prioritize documents containing query-specific keywords.
2. **Answer Generation**:
   - The top relevant documents are processed to extract the most relevant sentences, which are combined into a context.
   - The context is then truncated to fit within a token limit (`max_tokens`), ensuring compatibility with the language model.
   - The context and query are passed to the `google/flan-t5-large` model from **Hugging Face Transformers** to generate a detailed and contextually relevant answer.
3. **Confidence and Source Tracking**:
   - The system calculates confidence scores based on cosine similarity between the query and document embeddings, then provides the sources of the retrieved documents alongside the generated answer.
4. **Frontend-Backend Integration**:
   - A **FastAPI** backend handles document embedding, retrieval, and query processing.
   - A **React** frontend allows users to input questions and view answers in an intuitive interface.

---

### Why This Approach?

- **Semantic Understanding**: The system uses Sentence Transformers to retrieve documents based on semantic meaning, with a keyword boost for improved relevance.
- **High-Quality Answer Generation**: The `google/flan-t5-large` model generates detailed and contextually relevant answers.
- **Explainability**: Sources of retrieved documents are provided to enhance transparency and trust.
- **Modularity**: The architecture separates retrieval and generation, making it easy to upgrade components.
- **Scalability**: Cosine similarity and embeddings enable efficient handling of diverse document types and queries.

---

### Trade-offs/Limitations

- **Embedding Model Size**: The `all-MiniLM-L6-v2` model is fast but less accurate than larger models.
- **Answer Generation Quality**: Generated answers depends on the relevance of the retrieved documents and the `google/flan-t5-large` model's capabilities.
- **In-Memory Storage**: Embeddings are stored in memory, limiting scalability for large datasets; a vector database ike **FAISS** or **Pinecone** could resolve this.
- **Response Time**: Retrieval and model processing speed affect the pipeline's response time.
- **Context Truncation**: Context is truncated to fit token limits, which may omit relevant details.
- **Document Format Support**: Only plain text files are supported; other formats like PDFs require preprocessing.

---

### Tools/Libraries

**Backend:**

- **FastAPI**: For building a lightweight, high-performance backend API.
- **Pydantic**: Used as part of FastAPI for data validation and serialization.
- **Uvicorn**: ASGI server for running the FastAPI backend.
- **Sentence Transformers**: For generating high-quality document embeddings.
- **Hugging Face Transformers**: For leveraging the `google/flan-t5-large` model to generate answers.
- **Python**: Core programming language for backend development.

**Frontend:**

- **Node.js**: For managing frontend dependencies and running the development server.
- **React (Vite/TypeScript)**: For building a fast, interactive and type-safe frontend.
- **Material-UI (MUI)**: For creating a consistent and responsive frontend design.
- **npm**: For managing JavaScript packages and scripts.

---

## Prerequisites

Before setting up the project, ensure you have the following installed:

1. **Python**: Install `pyenv` to manage Python versions. Follow the [pyenv installation guide](https://github.com/pyenv/pyenv#installation).
2. **Node.js**: Required for the frontend. Install it from [Node.js official website](https://nodejs.org/).
3. **Git**: For cloning the repository. Install it from [Git](https://git-scm.com/).

---

## Quickstart

For users who want to get started quickly, follow these minimal steps:

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/JadeChan03/rag-qa-fullstack.git
   cd rag-qa-fullstack
   ```

2. **Start the Backend**:

   ```bash
   cd server
   pyenv install 3.10.0  # Only if not already installed
   pyenv local 3.10.0
   python3 -m venv venv
   source venv/bin/activate  # Use `venv\Scripts\activate` on Windows
   pip install -r requirements.txt
   uvicorn app:app --reload
   ```

3. **Start the Frontend**:
   Open a separate terminal:

   ```bash
   cd client
   npm install
   npm run dev
   ```

4. **Access the Application**:

   - **Backend**: Visit `http://127.0.0.1:8000/docs` for the Swagger UI.
   - **Frontend**: Open `http://localhost:5173` in your browser.

5. **Ask a Question**:
   - Type your question into the input field in the frontend and click "Submit."
   - The system will process the query and retrieve an answer from the documents.

For a detailed setup, refer to the following section ([Setup Instructions](#setup-instructions)).

---

## Setup Instructions

### Clone the Repository

```bash
git clone https://github.com/JadeChan03/rag-qa-fullstack.git
```

### Running The Application

1. Open **two terminal sessions**:

   - **Terminal 1**: For running the backend server.
   - **Terminal 2**: For running the frontend client.

2. Follow the setup instructions for both the backend and frontend in their respective terminal sessions.

### Backend Setup

2. **Navigate to the Server Directory**

   ```bash
   cd rag-qa-fullstack/server
   ```

3. **Set the Python Version Using pyenv**  
   <br>If you use `pyenv` to manage Python versions, you can set the local Python version for the project.

   1. Install Python 3.10.0 (if not already installed):

      ```bash
      pyenv install 3.10.0
      ```

   2. In the `server` directory, set the local Python version:

      ```bash
      pyenv local 3.10.0
      ```

   3. Verify the Python version `pyenv` is using:

      ```bash
      pyenv version
      ```

      Ensure the output matches the required version (e.g., `3.10.0`).

   **If you encounter SSL errors during Python installation via `pyenv`, follow the steps in the "Troubleshooting: SSL Certificate Errors with pyenv" section below.**

4. **Create and Activate the Virtual Environment**
   <br>To isolate dependencies and avoid conflicts, create a virtual environment.

   **_On macOS/Linux:_**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

   **_On Windows:_**

   ```bash
   python -m venv venv
   `\venv\Scripts\activate
   ```

6. **Install Dependencies**
   <br>Once the virtual environment is activated, install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

7. **Select the Correct Python Interpreter in Visual Studio Code**
   <br>To avoid dependency import errors, ensure that VS Code is using the correct Python interpreter:

   - Press `Cmd+Shift+P` (macOS) or `Ctrl+Shift+P` (Windows/Linux).
   - Search for and select **Python: Select Interpreter**.
   - Choose the interpreter located in the `venv` folder. For example, `server/venv/bin/python` or `server/venv/Scripts/python.exe`.

8. **Start the Backend Server**

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

## Troubleshooting

### SSL Certificate Errors

If you encounter SSL errors during Python installation via `pyenv`, follow these steps **_prior_** to reactivating your python version (`pyenv local 3.10.0`) and virtual environment (`source venv/bin/activate`):

#### For macOS (Homebrew):

1. **Install SSL Dependencies**:

   ```bash
   brew install openssl readline xz zlib
   ```

2. **Reinstall Python 3.10.0 with SSL Support**:

   ```bash
   export LDFLAGS="-L$(brew --prefix openssl)/lib"
   export CPPFLAGS="-I$(brew --prefix openssl)/include"
   export PKG_CONFIG_PATH="$(brew --prefix openssl)/lib/pkgconfig"

   env PYTHON_CONFIGURE_OPTS="--enable-shared --with-openssl=$(brew --prefix openssl)" pyenv install 3.10.0
   ```

3. **Verify SSL Installation**:
   <br>Test that Python has SSL support by running:
   ```bash
   python3
   >>> import ssl
   >>> print(ssl.OPENSSL_VERSION)
   ```

#### For Windows:

1. **Install SSL Dependencies**:
   <br>Download and install the necessary SSL libraries, such as OpenSSL, from [https://slproweb.com/products/Win32OpenSSL.html](https://slproweb.com/products/Win32OpenSSL.html). Ensure that the correct version for your system architecture (32-bit or 64-bit) is installed.

2. **Set Environment Variables**:
   <br>Configure the paths to the OpenSSL libraries in your environment variables:

   - Add the `bin` directory of OpenSSL (e.g., `C:\Program Files\OpenSSL-Win64\bin`) to your `PATH`.
   - Set the `INCLUDE` and `LIB` environment variables to point to the OpenSSL installation directories.

3. **Reinstall Python with OpenSSL Support**:
   <br>Use the following commands to reinstall Python via `pyenv-win` with OpenSSL:

   ```bash
   set "PYTHON_CONFIGURE_OPTS=--with-openssl=C:\Program Files\OpenSSL-Win64"
   pyenv install 3.10.0
   ```

4. **Verify SSL Installation**:
   <br>Test that Python has SSL support by running:

   ```bash
   python
   >>> import ssl
   >>> print(ssl.OPENSSL_VERSION)
   ```

### General Steps for All Platforms

#### Activate/Reactivate Virtual Environment

- Always create and activate a virtual environment for each project to isolate dependencies. If an existing virtual environment was created with a Python version lacking SSL support or compatible dependencies, delete and recreate it:

  ```bash
  rm -rf venv
  python -m venv venv
  source venv/bin/activate   # Use `venv\Scripts\activate` on Windows
  pip install -r requirements.txt
  ```

#### Update Tools:

- Keep your tools up to date to avoid compatibility issues:

  ```bash
  # macOS/Linux
  brew update && brew upgrade
  pyenv update

  # Windows (PowerShell)
  pyenv update
  ```

#### Managing Global Python Dependencies:

- If global Python dependencies are causing conflicts or clutter, consider cleaning them up:

  1.  View all globally installed Python dependencies:

  ```bash
  pip list
  ```

  2.  Uninstall All Python Packages

  ```bash
  pip freeze | xargs pip uninstall -y
  ```

  - WARNING: This will remove all global packages, which may affect other projects or system tools.
  - These commands apply only to the **_current_** Python environment (global or virtual) and do not affect `pyenv`

---

## Questions to Ask the Q&A System

### Working Questions Based on Sample Client Documents

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

### Known Errors Due to Wording

Some questions provide inaccurate or incomplete response due to wording. To improve accuracy, simplifying questions and/or rewording them into direct requests may help.

- "Who is working on Project Phoenix?"
  - Answer: John Smith \* Tech Lead: Alice Green (Incomplete)
- "Name everyone on Project Phoenix"

  - Answer: "Jane Doe (VP, Customer Success) _ Project Manager: John Smith _ Tech Lead: Alice Green \* Primary Users: Customer Support Team, End Customers" (Better)

- "What is the remote work policy?"
  - Answer: All remote work must comply with the company's data security and confidentiality policies (Incomplete)
- "Summarise the remote work policy"

  - Answer: **1. Security:** All remote work must comply with the company's data security and confidentiality policies. Eligibility:** Full-time employees with manager approval and a role suitable for remote work are eligible. Communication:** Remote employees are expected to be reachable via company-approved communication channels (Slack, Email, Video Conferencing) during work hours. (Better)

- "What is the deadline for completing mandatory cybersecurity training for all staff?"
  - Answer: August 1, 2024 (Incorrect)
- "What is the deadline for completing cybersecurity training for all staff?"

  - Answer: September 30th (Correct but incomplete)

- "What are the key initiatives planned to enhance customer retention in Q3 2025?"
  - Answer: Let's work together to make Q3 a successful quarter (Irrelevant)
- "How will customer retention be improved?"
  - Answer: Reduce average support ticket resolution time by 15% (Better but incomplete)

---

## Future Improvements

Improvements are focused on the RAG system rather than the application as a whole, with enhancements focused on the development of the actual product rather than the PoC.

1. **Scalability**:
   - Implement a vector database like **Pinecone**, **Weaviate**, or **FAISS** to handle larger datasets and improve retrieval efficiency.
2. **Support for More Document Types**:
   - Add preprocessing pipelines to handle formats like PDFs, Word documents, and spreadsheets.
3. **Improved Answer Generation**:
   - Fine-tune the language model for domain-specific queries and improve context handling to reduce truncation issues.
4. **Optimized Response Time**:
   - Implement caching, asynchronous processing, and batching of LLM requests to reduce latency.
5. **Embedding Model Upgrades**:
   - Explore larger or more accurate embedding models to improve retrieval precision without compromising performance (a lightweight model was chosen largely due to the fact that this is a PoC).
