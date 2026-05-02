import os
from src.data_loader import load_all_documents
from src.vectorstore import FaissVectorStore
from src.search import RAGSearch

if __name__ == "__main__":
    
    docs = load_all_documents("data")
    store = FaissVectorStore("faiss_store")

    if not os.path.exists("faiss_store/faiss.index"):
        print("[INFO] Creating new FAISS index...")
        store.build_from_documents(docs)
    else:
        print("[INFO] Loading existing FAISS index...")
        store.load()

    rag_search = RAGSearch()

    query = "What is Emotion detection?"
    summary = rag_search.search_and_summarize(query, top_k=3)

    print("Summary:", summary)