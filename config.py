import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    # OpenAI Configuration
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4")
    openai_temperature: float = 0.7
    openai_max_tokens: int = 2048
    
    # Banking API Configuration
    banking_api_url: str = os.getenv("BANKING_API_URL", "http://localhost:8000")
    banking_api_key: str = os.getenv("BANKING_API_KEY", "")
    banking_api_timeout: int = 30
    
    # Vector Database Configuration
    vector_db_url: str = os.getenv("VECTOR_DB_URL", "localhost:6333")
    vector_db_name: str = os.getenv("VECTOR_DB_NAME", "banking_knowledge_base")
    vector_embedding_model: str = "text-embedding-3-small"
    vector_chunk_size: int = 1000
    vector_chunk_overlap: int = 200
    
    # Database Configuration
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///banking.db")
    database_pool_size: int = int(os.getenv("DATABASE_POOL_SIZE", "10"))
    
    # Security Configuration
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    max_retries: int = int(os.getenv("MAX_RETRIES", "3"))
    timeout_seconds: int = int(os.getenv("TIMEOUT_SECONDS", "30"))
    enable_pii_masking: bool = True
    
    # Agent Configuration
    confidence_threshold: float = 0.7
    max_iterations: int = 10
    
    class Config:
        case_sensitive = False

settings = Settings()
