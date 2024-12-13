from pydantic import BaseSettings

class Settings(BaseSettings):
    # Application settings
    APP_NAME: str = "Core Package"
    APP_ENV: str = "development"  # Options: development, production, testing
    DEBUG: bool = True

    # Database settings
    DB_URL: str = "sqlite:///./test.db"

    # Authentication settings
    SECRET_KEY: str = "your-secret-key"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"  # Load variables from a .env file (optional)

# Singleton settings instance
settings = Settings()
