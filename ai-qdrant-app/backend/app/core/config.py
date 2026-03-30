from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Core Settings
    PROJECT_NAME: str
    QDRANT_HOST: str
    QDRANT_PORT: int
    COLLECTION_NAME: str
    VECTOR_SIZE: int
    
    # Missing API Keys - These must match the names in your .env exactly
    OPENAI_API_KEY: str
    GROQ_API_KEY: str
    ENV_MODE: str

    # This 'extra="ignore"' is the secret sauce to prevent your current crash
    model_config = SettingsConfigDict(
        env_file=".env", 
        extra="ignore"
    )

settings = Settings()