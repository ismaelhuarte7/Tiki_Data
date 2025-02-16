from flask import Flask
from flask_session import Session
from config import database
from config.database import db
from src.web import comandos, routes
    
session = Session()

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
    with app.app_context():
        db.create_all() 

    return app
