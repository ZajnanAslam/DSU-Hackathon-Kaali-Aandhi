from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    SUPABASE_URL: str = ""
    SUPABASE_ANON_KEY: str = ""
    SUPABASE_SERVICE_KEY: str = ""
    DATABASE_URL: str = ""
    REDIS_URL: str = ""
    JWT_SECRET: str = ""
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL_VISION: str = "gemini-1.5-flash"
    TELEGRAM_BOT_TOKEN: str = ""
    TELEGRAM_CHAT_ID: str = ""
    VERCEL_FRONTEND_URL: str = ""

    # ChromaDB
    CHROMA_MODE: str = "memory"
    
    # Email Alerts
    ALERT_EMAIL: str = ""
    ALERT_EMAIL_PASSWORD: str = ""
    ALERT_RECIPIENT_EMAIL: str = ""

    # OCR
    TESSERACT_PATH: str = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


@lru_cache
def get_settings() -> Settings:
    return Settings()
