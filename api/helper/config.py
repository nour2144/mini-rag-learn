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

    class Config:
        env_file = ".env"
        
def get_settings():
    return Settings()
