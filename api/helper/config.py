from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Application settings
    app_name: str
    app_version: str
    app_mode: str

    # File settings
    file_allowed_types: list[str]
    file_max_size_mb: int
    file_chunk_size: int
    folder_default_name: str

    # MongoDB settings
    mongo_url: str
    mongo_db_name: str

    # LLM settings
    generation_backend: str
    embedding_backend: str
    
    openai_api_key: str
    openai_api_url: str = None
    openai_api_embedding_model: str = None
    
    generation_model: str = None
    embedding_model: str = None
    embedding_dimension: int = None
    default_input_token_limit: int = None
    default_temperature: float = None
    default_max_tokens: int = None

    # VectorDB settings
    vector_db_backend: str


    class Config:
        env_file = ".env"
        
def get_settings():
    return Settings()
