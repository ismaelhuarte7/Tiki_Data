import os

class Config:
    DEBUG = False
    SESSION_TYPE = "filesystem"
    SECRET_KEY = os.environ.get("SECRET_KEY")
    MAILJET_API_KEY = '882491176762670da1ba3ecd96a2af7f'
    MAILJET_SECRET_KEY = '4db10d01bb3315ce8ca6da7df4a832d2'
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL_UNPOOLED")
    
