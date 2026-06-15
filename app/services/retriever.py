from pathlib import Path
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.config import settings

VECTOR_STORE_DIR = str(Path(__file__).parent.parent.parent / "vector_store")

_retriever = None

def get_retriever():
    global _retriever
    if _retriever is None:
        embeddings = GoogleGenerativeAIEmbeddings(
            model=settings.embedding_model,
            google_api_key=settings.google_api_key,
        )
        db = Chroma(
            persist_directory=VECTOR_STORE_DIR,
            embedding_function=embeddings,
        )
        _retriever = db.as_retriever(
            search_type="similarity",
            search_kwargs={"k": settings.retriever_k},
        )
    return _retriever

def retrieve_context(question: str) -> list[str]:
    retriever = get_retriever()
    docs = retriever.invoke(question)
    return [doc.page_content for doc in docs]
