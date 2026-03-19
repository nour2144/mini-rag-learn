from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str
    app_version: str
    app_mode: str

    class Config:
        env_file = ".env"
        
def get_settings():
    return Settings()
