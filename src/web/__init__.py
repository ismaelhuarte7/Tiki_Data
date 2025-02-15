from flask import Flask
from flask_session import Session
from src.web.routes import main_bp
from config import database
from config.database import db
from src.models.user import User
from src.models.game import Game
    
session = Session()

def create_app(config_class):
    app = Flask(__name__)
    app.config.from_object(config_class)

    database.init_app(app)

    session.init_app(app)
    with app.app_context():
        db.create_all() 
    
    app.register_blueprint(main_bp)

    return app
