from sentence_transformers import SentenceTransformer, util
from transformers import pipeline
import os

# Load SentenceTransformer for embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')

# Load Hugging Face's pipeline for large language model (LLM) inference
qa_model = pipeline("text2text-generation", model="google/flan-t5-large")

# Load and embed documents
def load_documents(directory):
    """
    Load documents from a directory.
    """
    documents = {}
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                documents[filename] = file.read()
    return documents

def embed_documents(documents):
    """
    Generate embeddings for documents.
    """
    return {filename: model.encode(content, convert_to_tensor=True) for filename, content in documents.items()}

# Find the most relevant documents and generate a synthesized answer using an LLM
def find_answer(query, documents, doc_embeddings, top_n=3, max_tokens=450, similarity_threshold=0.3):
    """
    Retrieve the top N most relevant documents based on cosine similarity to the query,
    truncate or chunk the context to fit within the token limit,
    and use an LLM to generate a synthesized and comprehensive answer.
    """
    # Encode the user's query into a vector
    query_embedding = model.encode(query, convert_to_tensor=True)

    # Compute similarity scores between the query and each document
    scores = {
        filename: util.pytorch_cos_sim(query_embedding, embedding).item()
        for filename, embedding in doc_embeddings.items()
    }

    # Sort the documents by similarity scores (descending) and select the top N
    top_matches = sorted(scores.items(), key=lambda item: item[1], reverse=True)[:top_n]

    # Check if the highest similarity score exceeds the threshold
    if not top_matches or max(score for _, score in top_matches) < similarity_threshold:
        return {
            "answer": "I'm sorry, but your question doesn't seem to be related to the available context. "
                      "Please ask a question relevant to the enterprise content.",
            "source": [],
            "confidence": 0.0
        }

    # Combine the content of the top N documents
    combined_context = "\n\n".join(
        f"(Source: {filename})\n{documents[filename]}" for filename, _ in top_matches
    )

    # Truncate the context to fit within the token limit
    truncated_context = combined_context[:max_tokens]

    # Use the LLM to generate a comprehensive answer
    llm_input = (
        f"Question: {query}\n"
        f"Context: {truncated_context}\n\n"
        f"Please provide a detailed and comprehensive answer to the question based on the context. "
        f"Include all relevant details and examples mentioned in the context. "
        f"If the question is not related to the context, state that you only have access to enterprise information. "
        f"If you do not know the answer, state that you do not know. Keep the answer within 800 characters."
    )
    llm_output = qa_model(llm_input, max_length=800, num_return_sequences=1)[0]['generated_text']

    # Ensure the output is within 800 characters
    detailed_answer = llm_output[:800]

    # Return the answer, sources, and average confidence score
    sources = [filename for filename, _ in top_matches]
    average_confidence = sum(score for _, score in top_matches) / len(top_matches)

    return {
        "answer": detailed_answer,
        "source": sources,
        "confidence": average_confidence
    }