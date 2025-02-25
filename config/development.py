import os
import redis
class Config:
    DEBUG = True
    SESSION_TYPE = "redis"  
    SESSION_REDIS = redis.from_url(os.environ.get("REDIS_URL"))
    SECRET_KEY = os.environ.get("SECRET_KEY")
    MAILJET_API_KEY = os.environ.get("MAILJET_API_KEY")
    MAILJET_SECRET_KEY = os.environ.get("MAILJET_SECRET_KEY")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER")
    BASE_URL = os.getenv("BASE_URL")
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True

    db_user = os.environ.get("db_user")
    db_password = os.environ.get("db_password")
    db_host = os.environ.get("db_host")
    db_name = os.environ.get("db_name")


    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}"
