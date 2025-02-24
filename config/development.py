import os
class Config:
    DEBUG = True
    SESSION_TYPE = "filesystem"  
    SECRET_KEY = os.environ.get("SECRET_KEY")
    MAILJET_API_KEY = '882491176762670da1ba3ecd96a2af7f'
    MAILJET_SECRET_KEY = '4db10d01bb3315ce8ca6da7df4a832d2'
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER")

    db_user = os.environ.get("db_user")
    db_password = os.environ.get("db_password")
    db_host = os.environ.get("db_host")
    db_name = os.environ.get("db_name")


    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}"
