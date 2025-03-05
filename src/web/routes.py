from flask import Blueprint, render_template, session
from config.config import env
from config.database import db
import os
from src.models import Player, User, Goal, Court, Match, Team ,News
from src.web.controllers.auth import bp as auth_bp
from src.web.controllers.player import bp as player_bp
from src.web.controllers.court import bp as court_bp
from src.web.controllers.news import bp as news_bp



def register(app):
    @app.route("/")
    def home():
        user = User.get_by_id(session.get('user', {}).get('id'))
        news = News.get_all()
        if 'user' not in session:
            session.clear()
        return render_template("home.html", user=user, news_list=news)
    
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("errors/404.html"), 404
    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template("errors/500.html"), 500
    app.register_blueprint(auth_bp)
    app.register_blueprint(player_bp)
    app.register_blueprint(news_bp)
    app.register_blueprint(court_bp)

