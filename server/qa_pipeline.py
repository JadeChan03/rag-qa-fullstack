from sentence_transformers import SentenceTransformer, util
from transformers import pipeline
import os
import nltk
from nltk.corpus import stopwords

# ensure stopwords are downloaded
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

# load models
model = SentenceTransformer('all-MiniLM-L6-v2')
qa_model = pipeline("text2text-generation", model="google/flan-t5-large")

# 1. DATA LOADING: Prepare text documents for processing
def load_documents(directory):
    return {
        filename: open(os.path.join(directory, filename), 'r', encoding='utf-8').read()
        for filename in os.listdir(directory) if filename.endswith(".txt")
    }

# 2. DATA INDEXING: store document embeddings into a vector database l(ie. FAISS or Pinecone) for efficient retrieval -- not implemented in this simplified version

# 3. GENERATE EMBEDDINGS: documents are converted into vector embeddings
def embed_documents(documents):
    return {filename: model.encode(content, convert_to_tensor=True) for filename, content in documents.items()}

# 4. RETRIEVE RELEVANT INFO: retrieve the most relevant documents to provide context for the LLM
def find_answer(query, documents, doc_embeddings, top_n=3, max_tokens=450, similarity_threshold=0.3, keyword_boost=0.5):
    # encode query and extract keywords
    query_embedding = model.encode(query, convert_to_tensor=True)
    keywords = set(word for word in query.lower().split() if word not in stop_words)

    # compute document scores via cosine similarity and apply keyword boost
    scores = {
        filename: util.pytorch_cos_sim(query_embedding, embedding).item() +
                  (keyword_boost if any(keyword in documents[filename].lower() for keyword in keywords) else 0)
        for filename, embedding in doc_embeddings.items()
    }

    # retrieve top n documents
    top_matches = sorted(scores.items(), key=lambda item: item[1], reverse=True)[:top_n]

    if not top_matches or max(score for _, score in top_matches) < similarity_threshold:
        return {"answer": "No relevant information found.", "source": [], "confidence": 0.0}

    # extract relevant sentences from top documents
    combined_context = ""
    current_length = 0
    for filename, _ in top_matches:
        sentences = documents[filename].split('. ')
        sentence_scores = {
            sentence: util.pytorch_cos_sim(query_embedding, model.encode(sentence, convert_to_tensor=True)).item() +
                      (keyword_boost if any(keyword in sentence.lower() for keyword in keywords) else 0)
            for sentence in sentences
        }
        sorted_sentences = sorted(sentence_scores.items(), key=lambda item: item[1], reverse=True)
        for sentence, score in sorted_sentences:
            if score >= similarity_threshold and current_length + len(sentence) <= max_tokens:
                combined_context += f"{sentence}. "
                current_length += len(sentence)

    # 5. AUGMENT LLM PROMPT: prompt engineering techniques are utilized to effectively communicate with the LLM in order to generate an accurate answer
    llm_input = f"Question: {query}\nContext: {combined_context}\n\nProvide a detailed answer based on the context."
    llm_output = qa_model(llm_input, max_length=800, num_return_sequences=1)[0]['generated_text']

    # return the answer, sources, and confidence
    sources = [filename for filename, _ in top_matches]
    average_confidence = sum(score for _, score in top_matches) / len(top_matches)
    return {
        "answer": llm_output[:800], 
        "source": sources, 
        "confidence": average_confidence
    }

    # 6. UPDATE EXTERNAL DATA: maintain current information for retrieval, asynchronously update the documents and update embedding representation of the documents -- not implemented in this simplified version