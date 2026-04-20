from functools import wraps
from flask import session, redirect, url_for, flash

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash("Debes iniciar sesión para acceder a esta página", "danger")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash("Debes iniciar sesión para acceder a esta página", "danger")
            return redirect(url_for('auth.login'))
            
        from src.models.user import User
        user = User.get_by_id(session['user']['id'])
        if not user or not getattr(user, 'is_admin', False):
            flash("No tienes permiso para realizar esta acción", "danger")
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function
