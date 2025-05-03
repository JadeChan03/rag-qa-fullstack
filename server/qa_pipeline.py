from sentence_transformers import SentenceTransformer, util
import os



# load the SentenceTransformer model for embeddings
# 'all-MiniLM-L6-v2' is a lightweight model suitable for semantic search
model = SentenceTransformer('all-MiniLM-L6-v2') 

# 1. LOAD AND EMBED DOCUMENTS
def load_documents(directory):
    documents = {}
    for filename in os.listdir(directory):
		# only process files with a .txt extension
        if filename.endswith(".txt"):
			 # open the file and read its contents
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                documents[filename] = file.read()
    return documents

# generate embeddings for all documents using SentenceTransformer model
# input: documents, keys: file names, values: file contents (dict)
# output: dictionary, keys: file names, values: embeddings (dict)
def embed_documents(documents):
    doc_embeddings = {}
    for filename, content in documents.items():
		# encode the document content into a vector representation
        doc_embeddings[filename] = model.encode(content, convert_to_tensor=True)
    return doc_embeddings

# 2. ANSWER QUESTIONS
# finds the most relevant document and its content to answer user query
# input: query (str), documents (dict), doc_embeddings (dict)
# output: name of most relevant document (str)
def find_answer(query, documents, doc_embeddings):
	# encode the user's query into a vector
    query_embedding = model.encode(query, convert_to_tensor=True)
	# compute similarity scores between the query and each document
    scores = {}
    for filename, embedding in doc_embeddings.items():
        score = util.pytorch_cos_sim(query_embedding, embedding).item()
        scores[filename] = score

    # identify the document with the highest similarity score to find the most relevant document
    best_match = max(scores, key=scores.get)
	# return the best match along with content
    return f"Best match: {best_match}\nContent: {documents[best_match]}"