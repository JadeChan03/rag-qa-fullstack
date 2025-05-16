# RAG QA Fullstack

A full-stack Question-Answering (QA) system that uses Retrieval-Augmented Generation (RAG) to provide accurate, contextually relevant answers from unstructured documents.

---

## Table of Contents

1. [Problem Interpretation](#problem-interpretation)
2. [Proposed Solution & Rationale](#proposed-solution--rationale)
   - [Chosen Technical Approach](#chosen-technical-approach)
   - [RAG Pipeline Summary](#rag-pipeline-summary)
3. [Tools/Libraries](#toolslibraries)
   - [Backend](#backend)
   - [Frontend](#frontend)
4. [Prerequisites](#prerequisites)
5. [Quickstart](#quickstart)
6. [Setup Instructions](#setup-instructions)
   - [Backend Setup](#backend-setup)
   - [Frontend Setup](#frontend-setup)
7. [Troubleshooting](#troubleshooting)
   - [Dependency-Environment Version Errors](#dependency-environment-version-errors)
   - [SSL Certificate Errors](#ssl-certificate-errors)
8. [Questions to Ask the QA System](#questions-to-ask-the-qa-system)
   - [Working Questions](#working-questions-based-on-sample-client-documents)
   - [Known Errors Due to Wording](#known-errors-due-to-wording)
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
2. **Answer Generation**:
   - The top relevant documents are processed to extract the most relevant sentences, which are combined into a context.
   - The context is then truncated to fit within a token limit (`max_tokens`), ensuring compatibility with the language model.
   - The context and query are passed to the `google/flan-t5-large` model from **Hugging Face Transformers** to generate a detailed and contextually relevant answer.
3. **Confidence and Source Tracking**:
   - Confidence scores for documents and sentences are computed through:
      1. ***Cosine Similarity***: used to compare the query embedding with document and sentence embeddings, ensures efficient and meaningful retrieval of information
      2. ***Keyword Boost***: applied to prioritize documents containing query-specific keywords.
   - ***Retrieve Relevant Documents***: extract the highest-scoring documents from the data
   - ***Retrieve Relevant Sentences to Create the Context***: extract the highest-scoring sentences from top documents to create the context for the llm
   - Document scores, document names (sources) and the generated answer are provided as a result
4. **Frontend-Backend Integration**:
   - A **FastAPI** backend handles document embedding, retrieval, and query processing.
   - A **React** frontend allows users to input questions and view answers in an intuitive interface.
   
### RAG Pipeline Summary

1. **Data Loading**: Prepare text documents for processing
2. **Data Indexing***: Store document embeddings into a vector database (ie. FAISS or Pinecone) for efficient retrieval
3. **Generate Embeddings**: Documents are converted into vector embeddings
4. **Retrieve Relevant Information**: Retrieve top-scoring sources (relevant sentences are extracted from top-scoring documents) to provide context for the LLM
5. **Augment LLM Prompt**: Prompt engineering techniques are utilized to effectively communicate with the LLM in order to generate an accurate answer
6. **Update External Data***: Maintain current information for retrieval, asynchronously update the documents and update embedding representation of the documents

*not implemented in this simplified version

---

### Why This Approach?

This approach leverages ***semantic understanding*** via Sentence Transformers and high-quality, ***hallucination-free*** answer generation using Flan-T5, an open-source LLM published by Google. Its ***modular architecture*** prioritises scalability, while also ensuring ***transparent results*** by listing sources.

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
   pyenv local 3.10.0 # ensures compatibility with dependencies
   # note: refer to "Backend Setup: Environment Configurations" if version errors occur 
   python3 -m venv venv
   source venv/bin/activate  # use `venv\Scripts\activate` on Windows
   pip install -r requirements.txt
   uvicorn app:app --reload # starts server
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
   - **Frontend**: Open `http://localhost:5173` in your browser or press `o + enter`.

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

3. **Environment Configurations**  

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

   4. Verify the Python version `python3` is using:
  
      ```bash
      which python3 # expected to point to a pyenv shim
      python3 --version # expected `Python 3.10.0`
      ```

      If `which python3` does not point to a pyenv shim (e.g., ~/.pyenv/shims/python3), continue with the following steps to correct this issue:

   5. **Edit your Shell Configuration** (e.g., `~/.zshrc` or `~/.bashrc`)

   ```bash
   nano ~/.zshrc # use a text editor to open your shell
   ```
   
   6. **Add the Following to your Shell Configuration File**
    
   ```bash
   export PATH="$(pyenv root)/shims:$PATH"
   ```
   7. **Reload Shell Configuration**

   ```bash
   source ~/.zshrc
   ```

   **Additional Troubleshooting**

   - If you encounter SSL errors during Python installation via `pyenv`, follow the steps in the ([Troubleshooting: SSL Certificate Errors](#ssl-certificate-errors)).

5. **Create and Activate the Virtual Environment**
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

   Access the frontend at `http://localhost:5173` or press `o + enter`.

---

## Troubleshooting

### Dependency-Environment Version Errors

If you are installing `requirements.txt` and encounter an error like:

   ```bash
   ERROR: Could not find a version that satisfies the requirement torch<2.0.0,>=1.11.0 (from versions: 2.6.0, 2.7.0)
   ```

The error indicates that the specified version range for the dependency (in this case, torch >=1.11.0,<2.0.0) is not available for your current Python environment or platform. This could be due to two reasons:

   1. The local environment was set (`pyenv local 3.10.0`) ***after*** the virtual environment was created. You must delete your virtual environment and create a new one in the correct environment. However, if Python 3.10.0 was set with `pyenv` ***prior*** to creating the virtual environment. The issue likely arised because
   2. the Python version managed by `pyenv` (3.10.0) is not properly linked to the `python3` command when creating the virtual environment. Even though you set pyenv local 3.10.0, the python3 command might still point to a system-installed Python version (e.g., 3.13.0) instead of the pyenv-managed version. To fix this, refer to steps 5-7 in ([Environment Configuration](environment-configuation).

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

#### Ensure pyenv is Properly Set Up:

- Make sure pyenv (or pyenv-win for Windows) is initialized in your shell configuration file (e.g., `.bashrc` or `.zshrc` for macOS/Linux, or `PowerShell` for Windows).

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

#### Recreate Virtual Environment:

- Always create and activate a virtual environment for each project to isolate dependencies. If an existing virtual environment was created with a Python version lacking SSL support or compatible dependencies, delete and recreate it:

  ```bash
  rm -rf venv
  python -m venv venv
  source venv/bin/activate   # Use `venv\Scripts\activate` on Windows
  pip install -r requirements.txt
  ```

---

## Questions to Ask the QA System

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
- "Name everyone on Project Phoenix?"
   - Answer: Jane Doe (VP, Customer Success) (Incomplete)
- "Name everyone on Project phoenix" ***('Phoenix' is lower case)***
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
6. **Enhance Prompt Transparency**:
   - Explicitly provide the segment that prooves that generated answer, and a link to the full source document(s).
7. **Leverage LangChain for Pipeline Simplification**:
   - Integrate the LangChain framework to streamline the handling of document loading, embedding generation, vector database integration, and LLM interaction.
   - Use LangChain's modular components to simplify the addition of new features, such as prompt templates, memory for chatbots, and tool chaining.
   - This would reduce development overhead and improve maintainability as the system scales.