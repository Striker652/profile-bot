import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()

SOURCE_DIR = Path(__file__).parent.parent / "data" / "sources"
VECTOR_STORE_DIR = Path(__file__).parent.parent / "vector_store"

def ingest():
    print("Loading source documents...")
    loader = DirectoryLoader(SOURCE_DIR, glob="**/*.md", loader_cls=TextLoader)
    docs = loader.load()
    print(f"  Loaded {len(docs)} documents")

    print("Splitting into chunks...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", ". ", " "],
    )
    chunks = splitter.split_documents(docs)
    print(f"  Created {len(chunks)} chunks")

    print("Embedding and persisting to Chroma...")
    embeddings = GoogleGenerativeAIEmbeddings(
        model=os.getenv("EMBEDDING_MODEL", "models/gemini-embedding-001"),
        google_api_key=os.getenv("GOOGLE_API_KEY"),
    )
    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(VECTOR_STORE_DIR),
    )
    print(f"  Vector store saved to {VECTOR_STORE_DIR}")
    print("Ingestion complete.")

if __name__ == "__main__":
    ingest()
