import os
import redis
from urllib.parse import quote_plus

class Config:
    DEBUG = False
    SESSION_TYPE = "redis"  
    SESSION_REDIS = redis.from_url(os.environ.get("REDIS_URL"))
    SECRET_KEY = os.environ.get("SECRET_KEY")
    MAILJET_API_KEY = os.getenv("MAILJET_API_KEY", "")
    MAILJET_SECRET_KEY = os.getenv("MAILJET_SECRET_KEY", "")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER", "noreply@localhost")
    BASE_URL = os.getenv("BASE_URL")
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Almacenamiento local para imágenes (Railway tiene volúmenes persistentes)
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max
    
    # Base de datos MySQL (Railway proporciona estas variables)
    db_user = os.environ.get("db_user") or os.environ.get("MYSQLUSER")
    db_password = os.environ.get("db_password") or os.environ.get("MYSQLPASSWORD")
    db_host = os.environ.get("db_host") or os.environ.get("MYSQLHOST")
    db_name = os.environ.get("db_name") or os.environ.get("MYSQLDATABASE")
    db_port = os.environ.get("db_port") or os.environ.get("MYSQLPORT", "3306")
    
    # URL encode del password para manejar caracteres especiales
    db_password_encoded = quote_plus(db_password) if db_password else ""
    
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{db_user}:{db_password_encoded}@{db_host}:{db_port}/{db_name}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
