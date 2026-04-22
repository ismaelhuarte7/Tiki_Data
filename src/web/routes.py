from flask import Blueprint, render_template, session, send_from_directory, request, redirect, url_for
from config.config import env
from config.database import db
import os
from src.models import Player, User, Goal, Court, Match, Team, News, Notification
from src.web.controllers.auth import bp as auth_bp
from src.web.controllers.player import bp as player_bp
from src.web.controllers.court import bp as court_bp
from src.web.controllers.news import bp as news_bp
from src.web.controllers.match import bp as match_bp
from src.web.controllers.notification import bp as notification_bp
from src.services.match_service import MatchService



def register(app):
    @app.before_request
    def require_auth_for_private_pages():
        endpoint = request.endpoint
        if not endpoint:
            return None

        public_endpoints = {
            'home',
            'auth.login',
            'auth.signup',
            'auth.verify',
            'static',
        }

        if endpoint in public_endpoints:
            return None

        if endpoint.startswith('auth.') and endpoint in {'auth.login', 'auth.signup', 'auth.verify'}:
            return None

        if 'user' not in session:
            return redirect(url_for('home'))

        MatchService.finalize_expired_mvp_votes()

        return None

    @app.route("/")
    def home():
        user = None
        if 'user' not in session:
            session.clear()
            return render_template("landing.html")
        else:
            user = User.get_by_id(session['user']['id'])
            
        page = request.args.get('page', 1, type=int)
        news_pagination = News.query.order_by(News.created_at.desc()).paginate(
            page=page, per_page=5, error_out=False
        )
        return render_template("home.html", user=user, news_pagination=news_pagination)
    
    # Ruta para servir archivos subidos (imágenes)
    @app.route('/uploads/<path:filename>')
    def uploaded_file(filename):
        upload_folder = app.config.get('UPLOAD_FOLDER', 'uploads')
        return send_from_directory(upload_folder, filename)
    
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("errors/404.html"), 404
    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template("errors/500.html"), 500
    
    # Context processor para agregar notificaciones a todas las plantillas
    @app.context_processor
    def inject_notifications():
        notifications = []
        notification_count = 0
        if 'user' in session:
            user_id = session['user']['id']
            notifications = Notification.get_by_user(user_id)
            notification_count = len(notifications)
        return dict(user_notifications=notifications, notification_count=notification_count)
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(player_bp)
    app.register_blueprint(news_bp)
    app.register_blueprint(court_bp)
    app.register_blueprint(match_bp)
    app.register_blueprint(notification_bp)

