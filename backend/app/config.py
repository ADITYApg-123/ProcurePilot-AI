"""
Application configuration.
Loads environment variables and provides app-wide settings.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""

    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = "gemini-2.5-flash"

    # Upload settings
    UPLOAD_DIR: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "uploads")
    MAX_FILE_SIZE_MB: int = 10
    ALLOWED_EXTENSIONS: set = {".pdf"}

    # Extraction settings
    MAX_EXTRACTION_RETRIES: int = 3

    # Scoring defaults (user-configurable via API)
    DEFAULT_COST_WEIGHT: float = 0.4
    DEFAULT_WARRANTY_WEIGHT: float = 0.3
    DEFAULT_DELIVERY_WEIGHT: float = 0.3


settings = Settings()

# Ensure upload directory exists
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
