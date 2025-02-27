from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from src.models import News, User

bp = Blueprint("news", __name__, url_prefix="/news")

@bp.route('/create', methods=['GET', 'POST'])
def create():
    if 'user' not in session:
        flash("Debes iniciar sesión para crear una noticia", "danger")
        return redirect(url_for('auth.login'))

    user = User.get_by_id(session['user']['id'])
    if not user.is_admin:
        flash("No tienes permiso para crear una noticia", "danger")
        return redirect(url_for('home'))

    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")

        if not title or not content:
            flash("Todos los campos son obligatorios", "danger")
            return render_template("news/create.html")

        News.create(title=title, content=content, user_id=user.id)
        flash("Noticia creada correctamente", "success")
        return redirect(url_for('home'))

    return render_template("news/create.html")