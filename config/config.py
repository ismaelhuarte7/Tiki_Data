import os

env = os.getenv("FLASK_ENV")

if env == "production":
    from config.production import Config
else:
    from config.development import Config
