from flask import Blueprint, render_template, session
from config.config import env
from config.database import db
import os
from src.models import Player, User, Goal, Court, Match, Team 
from src.web.controllers.auth import bp as auth_bp



def register(app):
    @app.route("/")
    def home():
        users = User.get_all_users()
        print("variables de entorno", os.getenv("BREVO_EMAIL"), os.getenv("BREVO_PASSWORD"), os.getenv("MAIL_SENDER"), os.getenv("FLASK_ENV"), os.getenv("SECRET_KEY"))
        return render_template("home.html", users=users)
    
    @app.route('/verificar')
    def verificar():
        # Recupera el valor de la sesión
        usuario = session.get('usuario', 'No hay usuario en la sesión')
        return f"Usuario en sesión: {usuario}"
    app.register_blueprint(auth_bp)

