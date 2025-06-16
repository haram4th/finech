from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "mysql+pymysql://root:password@localhost:3307/stock_news")
    
    # API Keys
    FINNHUB_API_KEY: str = os.getenv("FINNHUB_API_KEY", "")
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    
    # CORS settings
    CORS_ORIGINS: list = ["http://localhost:5173", "http://localhost:5174"]
    
    # JWT
    SECRET_KEY: str = "your-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # News API settings
    NEWS_CACHE_TIMEOUT: int = 3600  # 1 hour
    MAX_NEWS_PER_REQUEST: int = 10
    
    # Model settings
    PREDICTION_WINDOW: int = 7  # 7 days prediction
    
    class Config:
        env_file = ".env"

settings = Settings() 