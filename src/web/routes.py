from flask import Blueprint, render_template
from config.config import env
from config.database import db
from src.models.user import User

def register(app):
    @app.route("/")
    def home():
        users = User.get_all_users()
        return render_template("home.html", users=users)



