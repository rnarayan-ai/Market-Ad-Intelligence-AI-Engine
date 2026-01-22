from langchain_community.vectorstores import FAISS
#from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings


embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def build_vector_db(texts):
    return FAISS.from_texts(texts, embeddings)

def search_vector_db(db, query, k=3):
    return db.similarity_search(query, k=k)
