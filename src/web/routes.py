from flask import Blueprint, render_template, send_from_directory
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
    @app.route("/logo")
    def logo():
        return send_from_directory("static/img", "logo.png")
    app.register_blueprint(auth_bp)

