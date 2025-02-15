import os

class Config:
    DEBUG = False
    SESSION_TYPE = "filesystem"  
    db_user = os.getenv("AZURE_SQL_USER")
    db_password = os.getenv("AZURE_SQL_PASSWORD")
    db_host = os.getenv("AZURE_SQL_HOST")
    db_name = os.getenv("AZURE_SQL_DATABASE")
    db_port = os.getenv("AZURE_SQL_PORT")

    print(f"Database URI Producrion: {db_user}:{db_password}@{db_host}:{db_port}/{db_name}")

    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"