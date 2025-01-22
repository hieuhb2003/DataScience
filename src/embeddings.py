from langchain_community.vectorstores import FAISS
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)

def setup_embeddings():
    # Khởi tạo embedding model
    embedding_function = SentenceTransformerEmbeddings(model_name="BAAI/bge-m3")
    
    # Load FAISS index
    db = FAISS.load_local(
        "models/laptop_db",
        embedding_function,
        allow_dangerous_deserialization=True
    )
    
    return db.as_retriever()