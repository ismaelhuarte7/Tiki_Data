import os

class Config:
    DEBUG = False
    SESSION_TYPE = "filesystem"  
    db_user = os.getenv("AZURE_MYSQL_USER")
    db_password = os.getenv("AZURE_MYSQL_PASSWORD")
    db_host = os.getenv("AZURE_MYSQL_HOST")
    db_name = os.getenv("AZURE_MYSQL_NAME")

    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}"