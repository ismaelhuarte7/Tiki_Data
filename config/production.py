import os

class Config:
    DEBUG = False
    SESSION_TYPE = "filesystem"

    # Obtiene la URL completa desde la variable de entorno
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL_UNPOOLED")
    

    print(f"Database URI Production: {SQLALCHEMY_DATABASE_URI}")
