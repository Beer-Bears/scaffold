from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # Project settings
    project_name: str = "Scaffold"
    project_description: str = "Specialized RAG system for large codebases"
    version: str = "0.1.0"
    environment: str = "development"
    
    # Database settings
    postgres_enabled: bool = True
    neo4j_enabled: bool = True
    
    # LLM settings
    llm_model: str = "scaffold-llm-v1"
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings() 