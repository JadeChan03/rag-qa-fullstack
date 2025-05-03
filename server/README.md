# Client Document Q&A System - Proof of Concept (PoC)

## Problem Interpretation
The client, a medium-sized enterprise, faces significant inefficiencies due to employees spending excessive time searching through internal documents (e.g., product specifications, HR policies, project reports) to find answers to common questions. This impacts overall productivity. 

The goal of this Proof of Concept (PoC) is to develop a simple internal tool that allows employees to ask questions in natural language and receive concise, accurate answers derived solely from a curated set of company documents. This tool will demonstrate the feasibility and value of using AI to address this problem.

---

## Proposed Solution & Rationale

### Solution Overview
This PoC implements a Question-Answering (QA) system that:
1. **Processes Documents**: Ingests and indexes the provided text documents for efficient retrieval.
2. **Answers Questions**: Accepts a user's natural language question as input.
3. **Generates Grounded Answers**: Synthesizes answers solely based on the information in the provided documents, ensuring relevance, accuracy, and clarity.

### Technical Approach
1. **Document Processing**:
   - **SentenceTransformers**: Used to generate embeddings for the provided .txt files. This enables semantic understanding of document content.
   - **FAISS**: Used as a lightweight and efficient vector database for storing and querying document embeddings.

2. **Question Answering**:
   - **SentenceTransformers**: Also used to encode user questions for semantic similarity comparison.
   - **Cosine Similarity**: Used to match user questions with the most relevant document content.

3. **Libraries and Tools**:
   - **FastAPI**: Provides a simple REST API interface for user interaction with the system.
   - **SentenceTransformers**: A robust tool for embedding generation with pre-trained models.
   - **FAISS**: Ensures fast and scalable similarity searches.
   - **Python**: Chosen for its rich ecosystem of AI/ML libraries and ease of use.

### Rationale
- **Accuracy**: By using SentenceTransformers and FAISS, the system retrieves the most semantically relevant content.
- **Relevance**: Cosine similarity ensures only the closest matching content is used for answers.
- **Clarity**: The concise REST API interface ensures simplicity in user interaction.
- **Feasibility**: All tools and libraries used are open-source and well-documented, ensuring reproducibility and ease of extension.

### Trade-offs
- **Performance vs Simplicity**: FAISS is chosen for simplicity over more complex tools like ElasticSearch, given the small dataset provided.
- **Pre-trained Models**: Using pre-trained embeddings limits customization but ensures rapid development.

---

## Setup Instructions

### 1. Prerequisites
- Python 3.10 or higher installed on your system.
- A terminal or shell to run commands.

### 2. Clone the Repository
```bash
git clone https://github.com/your-repo-name.git
cd your-repo-name
```

### 3. Create a Virtual Environment
```bash
python3 -m venv rag_env
source rag_env/bin/activate  # On Windows: rag_env\Scripts\activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Organize Documents
Place the `.txt` files in a `documents/` folder within the project directory.

### 6. Run the Application
Start the FastAPI application:
```bash
uvicorn app:app --reload
```

Access the API Swagger UI at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

---

## How to Use

1. Start the FastAPI server as described in the setup instructions.
2. Navigate to the Swagger UI at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).
3. Use the `/ask` endpoint to ask a question. Example JSON input:
   ```json
   {
     "query": "What is the company's HR policy on leave?"
   }
   ```
4. The system will return a concise answer based on the provided documents.

---

## Limitations & Next Steps

### Limitations
- **Small Dataset**: This PoC is limited to a small number of `.txt` files. Scaling to larger datasets may require more advanced indexing tools (e.g., ElasticSearch).
- **Answer Quality**: The system uses semantic similarity but does not generate fully structured answers.
- **Document Formats**: Currently supports only `.txt` files.

### Next Steps
1. **Scalability**: Extend the system to handle larger and diverse document collections.
2. **Answer Generation**: Integrate more advanced techniques for generating structured answers (e.g., fine-tuned generative models).
3. **Document Types**: Expand support for other formats like PDFs, Word documents, and spreadsheets.
4. **Improved Relevance**: Experiment with more advanced retrievers and ranking mechanisms for better relevance.

---

## Evaluation Criteria
This PoC fulfills the following client requirements:
- **Accuracy**: Answers are grounded in the provided documents through semantic similarity.
- **Relevance**: Retrieval of the most relevant document sections is prioritized.
- **Clarity**: The FastAPI interface ensures simplicity for end-users.
- **Reproducibility**: Clear setup instructions enable easy reproduction of results.

---