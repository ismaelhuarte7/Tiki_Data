from dotenv import load_dotenv

# Cargar variables de entorno ANTES de importar Config
load_dotenv()

from src.web import create_app
from config.config import Config

app = create_app(Config)

if __name__ == "__main__":
    app.run()
