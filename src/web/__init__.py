from flask import Flask
from flask_session import Session
from config import database
from config.database import db
from src.web import comandos, routes
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate

session = Session()
csrf = CSRFProtect()
migrate = Migrate()

def create_app(config_class):
    app = Flask(__name__)
    # Comandos
    comandos.register(app)
    # Configuración
    app.config.from_object(config_class)
    # Rutas

    routes.register(app)
    # Inicialización de la base de datos
    database.init_app(app)
    session.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)

    @app.after_request
    def force_utf8(response):
        content_type = response.headers.get('Content-Type', '')
        if content_type.startswith('text/html') or content_type.startswith('text/plain'):
            response.headers['Content-Type'] = f"{content_type.split(';')[0]}; charset=utf-8"
        return response



    return app
