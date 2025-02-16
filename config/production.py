import os

class Config:
    DEBUG = False
    SESSION_TYPE = "filesystem"
    db_user = os.getenv("AZURE_SQL_USER")
    db_password = os.getenv("AZURE_SQL_PASSWORD")
    db_host = os.getenv("AZURE_SQL_SERVER")
    db_name = os.getenv("AZURE_SQL_DATABASE")
    db_port = os.getenv("AZURE_SQL_PORT", 1433)

    print ("host: ----------- ", db_host)

    print(f"Database URI Production: {db_user}:{db_password}@{db_host}:{db_port}/{db_name}")

    SQLALCHEMY_DATABASE_URI = (
    f"mssql+pyodbc://{db_user}:{db_password}@{db_host}:{db_port}/"
    f"{db_name}?driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes"
)

    
