import os
import redis
from urllib.parse import quote_plus


def _to_bool(value, default=False):
    if value is None:
        return default
    return value.strip().lower() in ("1", "true", "yes", "on")

class Config:
    DEBUG = False
    SECRET_KEY = os.environ.get("SECRET_KEY")
    REQUIRE_EMAIL_VERIFICATION = _to_bool(os.environ.get("REQUIRE_EMAIL_VERIFICATION"), True)
    
    # SMTP (Gmail)
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.gmail.com").strip()
    MAIL_PORT = int(os.environ.get("MAIL_PORT", 587))
    MAIL_USE_TLS = _to_bool(os.environ.get("MAIL_USE_TLS"), True)
    MAIL_USE_SSL = _to_bool(os.environ.get("MAIL_USE_SSL"), False)
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME", "").strip()
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD", "").strip()
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER", MAIL_USERNAME).strip()
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
    
    # Cloudinary para almacenamiento de imágenes
    # Limpiar espacios en blanco de las variables
    CLOUDINARY_CLOUD_NAME = os.environ.get("CLOUDINARY_CLOUD_NAME", "").strip()
    CLOUDINARY_API_KEY = os.environ.get("CLOUDINARY_API_KEY", "").strip()
    CLOUDINARY_API_SECRET = os.environ.get("CLOUDINARY_API_SECRET", "").strip()
    
    # Validar configuración de Cloudinary
    if not all([CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET]):
        print("WARNING: Cloudinary no configurado, usando almacenamiento local")
        USE_CLOUDINARY = False
        UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'uploads')
    else:
        USE_CLOUDINARY = True
        print(f"INFO: Cloudinary configurado - Cloud: {CLOUDINARY_CLOUD_NAME}, API Key: {CLOUDINARY_API_KEY[:8]}...")
    
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

    if REQUIRE_EMAIL_VERIFICATION and (not MAIL_USERNAME or not MAIL_PASSWORD):
        raise ValueError(
            "ERROR: REQUIRE_EMAIL_VERIFICATION=true pero faltan MAIL_USERNAME/MAIL_PASSWORD en producción."
        )
    
