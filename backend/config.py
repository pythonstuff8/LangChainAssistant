"""Configuration settings for the LangChain RAG Assistant backend."""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # OpenAI Configuration
    openai_api_key: str = ""
    openai_chat_model: str = "gpt-4o-mini"
    openai_embedding_model: str = "text-embedding-3-small"
    
    # RAG Configuration
    chunk_size: int = 1000
    chunk_overlap: int = 200
    
    # Vector Store Configuration
    chroma_persist_directory: str = "./data/chroma_db"
    collection_name: str = "langchain_docs"
    
    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 3005
    
    # Documentation URLs
    langchain_docs_url: str = "https://python.langchain.com/docs"
    langgraph_docs_url: str = "https://langchain-ai.github.io/langgraph"
    langsmith_docs_url: str = "https://docs.smith.langchain.com"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
