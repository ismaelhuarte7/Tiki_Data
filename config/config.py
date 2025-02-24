import os

env = os.getenv("FLASK_ENV")
secret_key = os.getenv("SECRET_KEY")



if env == "production":
    from config.production import Config
else:
    from config.development import Config
