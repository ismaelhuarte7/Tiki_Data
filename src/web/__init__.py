from flask import Flask
from flask_session import Session
from flask_mail import Mail
from config import database
from config.database import db
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

session = Session()
csrf = CSRFProtect()
migrate = Migrate()
mail = Mail()
scheduler = BackgroundScheduler()

def create_app(config_class):
    app = Flask(__name__)
    # Configuración
    app.config.from_object(config_class)

    from src.web import comandos, routes

    # Comandos
    comandos.register(app)
    # Rutas

    routes.register(app)
    # Inicialización de la base de datos
    database.init_app(app)
    session.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    # Inicializar scheduler para tareas programadas
    from src.web.scheduler import init_scheduler, shutdown_scheduler
    init_scheduler(app)
    atexit.register(shutdown_scheduler)

    @app.after_request
    def force_utf8(response):
        content_type = response.headers.get('Content-Type', '')
        if content_type.startswith('text/html') or content_type.startswith('text/plain'):
            response.headers['Content-Type'] = f"{content_type.split(';')[0]}; charset=utf-8"
        return response


    return app
