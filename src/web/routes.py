from flask import Blueprint, render_template
from config.config import env
from config.database import db
from src.models import Player, User, Goal, Court, Match, Team 
from src.web.controllers.auth import bp as auth_bp



def register(app):
    @app.route("/")
    def home():
        users = User.get_all_users()
        return render_template("home.html", users=users)
    app.register_blueprint(auth_bp)
