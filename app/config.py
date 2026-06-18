from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    google_api_key: str = ""
    allowed_origins: str = "http://localhost:5173,https://striker652.github.io"
    langsmith_api_key: str = ""
    vector_store_gcs_uri: str = ""
    chat_model: str = "gemini-2.5-flash"
    embedding_model: str = "models/gemini-embedding-001"
    retriever_k: int = 4
    portfolio_owner_name: str = "Nomula Hemanth Reddy"

    class Config:
        env_file = ".env"

settings = Settings()
