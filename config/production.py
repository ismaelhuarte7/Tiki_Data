import os
import redis
from urllib.parse import quote_plus

class Config:
    DEBUG = False
    SECRET_KEY = os.environ.get("SECRET_KEY")
    MAILJET_API_KEY = os.getenv("MAILJET_API_KEY", "")
    MAILJET_SECRET_KEY = os.getenv("MAILJET_SECRET_KEY", "")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER", "noreply@localhost")
    BASE_URL = os.getenv("BASE_URL")
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Configuración de Redis para sesiones
    # Railway puede proporcionar REDIS_URL o variables separadas
    redis_url = os.environ.get("REDIS_URL") or os.environ.get("REDIS_PRIVATE_URL")
    
    if not redis_url:
        # Construir URL desde variables separadas
        redis_host = os.environ.get("REDISHOST")
        redis_port = os.environ.get("REDISPORT", "6379")
        redis_user = os.environ.get("REDISUSER", "default")
        redis_password = os.environ.get("REDISPASSWORD")
        
        if redis_host and redis_password:
            redis_url = f"redis://{redis_user}:{redis_password}@{redis_host}:{redis_port}"
    
    if redis_url:
        SESSION_TYPE = "redis"
        SESSION_REDIS = redis.from_url(redis_url)
    else:
        # Fallback a filesystem si no hay Redis
        SESSION_TYPE = "filesystem"
        print("WARNING: Redis no configurado, usando sesiones en filesystem")
    
    # Almacenamiento local para imágenes (Railway tiene volúmenes persistentes)
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max
    
    # Base de datos MySQL (Railway proporciona estas variables)
    db_user = os.environ.get("db_user") or os.environ.get("MYSQLUSER")
    db_password = os.environ.get("db_password") or os.environ.get("MYSQLPASSWORD")
    db_host = os.environ.get("db_host") or os.environ.get("MYSQLHOST")
    db_name = os.environ.get("db_name") or os.environ.get("MYSQLDATABASE")
    db_port = os.environ.get("db_port") or os.environ.get("MYSQLPORT", "3306")
    
    # Validar variables de MySQL
    if not all([db_user, db_password, db_host, db_name]):
        missing = []
        if not db_user: missing.append("MYSQLUSER")
        if not db_password: missing.append("MYSQLPASSWORD")
        if not db_host: missing.append("MYSQLHOST")
        if not db_name: missing.append("MYSQLDATABASE")
        raise ValueError(
            f"ERROR: Faltan variables de entorno de MySQL: {', '.join(missing)}. "
            "Verifica que el servicio MySQL esté agregado en Railway."
        )
    
    # URL encode del password para manejar caracteres especiales
    db_password_encoded = quote_plus(db_password)
    
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{db_user}:{db_password_encoded}@{db_host}:{db_port}/{db_name}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
