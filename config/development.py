import os
import redis
from urllib.parse import quote_plus

class Config:
    DEBUG = True
    
    # Sesiones: Intenta usar Redis si está disponible, sino usa filesystem
    REDIS_URL = os.environ.get("REDIS_URL")
    if REDIS_URL:
        SESSION_TYPE = "redis"
        try:
            SESSION_REDIS = redis.from_url(REDIS_URL)
        except:
            SESSION_TYPE = "filesystem"
            SESSION_FILE_DIR = os.path.join(os.path.dirname(__file__), '..', 'flask_session')
    else:
        SESSION_TYPE = "filesystem"
        SESSION_FILE_DIR = os.path.join(os.path.dirname(__file__), '..', 'flask_session')
    
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")
    
    # Resend para emails
    RESEND_API_KEY = os.environ.get("RESEND_API_KEY", "")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER", "onboarding@resend.dev")
    BASE_URL = os.getenv("BASE_URL", "http://localhost:5000")
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    
    # Cloudinary para almacenamiento de imágenes (opcional en desarrollo)
    CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
    CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
    CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")
    
    USE_CLOUDINARY = all([CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET])
    
    # Almacenamiento local para imágenes (fallback)
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max

    db_user = os.environ.get("db_user", "root")
    db_password = os.environ.get("db_password", "")
    db_host = os.environ.get("db_host", "localhost")
    db_name = os.environ.get("db_name", "tiki_db")

    # URL encode del password para manejar caracteres especiales
    db_password_encoded = quote_plus(db_password) if db_password else ""
    
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{db_user}:{db_password_encoded}@{db_host}/{db_name}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
