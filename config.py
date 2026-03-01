import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    
    LM_STUDIO_API_URL = os.getenv("LM_STUDIO_API_URL", "http://localhost:1234/v1")
    LM_STUDIO_MODEL = os.getenv("LM_STUDIO_MODEL", "neural-chat")
    
    APP_HOST = os.getenv("APP_HOST", "127.0.0.1")
    APP_PORT = int(os.getenv("APP_PORT", 8080))
    DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() == "true"
    
    MAX_UPLOAD_SIZE_MB = int(os.getenv("MAX_UPLOAD_SIZE_MB", 50))
    MAX_UPLOAD_SIZE_BYTES = MAX_UPLOAD_SIZE_MB * 1024 * 1024
    SUPPORTED_FORMATS = os.getenv("SUPPORTED_FORMATS", "pdf,txt,docx,md").split(",")
    
    UPLOADS_DIR = os.path.join(os.path.dirname(__file__), "uploads")
    
    os.makedirs(UPLOADS_DIR, exist_ok=True)


config = Config()
