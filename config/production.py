import os
import redis
class Config:
    DEBUG = False
    SESSION_TYPE = "redis"  
    SESSION_REDIS = redis.from_url(os.environ.get("REDIS_URL"))
    SECRET_KEY = os.environ.get("SECRET_KEY")
    MAILJET_API_KEY = os.getenv("MAILJET_API_KEY")
    MAILJET_SECRET_KEY = os.getenv("MAILJET_SECRET_KEY")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL_UNPOOLED")
    BASE_URL = os.getenv("BASE_URL")
    
