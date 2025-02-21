from flask import Flask
from flask_mailman import Mail
from flask_session import Session
import os
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

    app.config['MAIL_SERVER'] = 'smtp-relay.brevo.com'  
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.getenv("BREVO_EMAIL") 
    app.config['MAIL_PASSWORD'] = os.getenv("BREVO_PASSWORD")
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv("MAIL_SENDER")  
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    mail = Mail(app)
    mail.init_app(app)


    # Rutas
    routes.register(app)

    # Inicialización de la base de datos
    database.init_app(app)
    session.init_app(app)
    with app.app_context():
        db.create_all() 

    return app
