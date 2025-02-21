from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask import session
from src.models import User, Player

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route('/sign_up', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        username = request.form["username"]
        name = request.form["first_name"]
        surname = request.form["last_name"]
        birth_date = request.form["birthdate"]
        
        if User.get_by_email(email):
            flash("El email ya está en uso.", "danger")
            return redirect(url_for("auth.signup"))
        if User.get_by_username(username):
            flash("El nombre de usuario ya está en uso.", "danger")
        player = Player.create(name, surname, birth_date)
        user = User.create(username, email, password, player.id)
        flash("Usuario creado correctamente", "success")
        return redirect(url_for("auth.login"))
    
    return render_template("auth/sign_up.html")

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = User.get_by_email(email)
        if not user:
            flash("Usuario no encontrado", "danger")
            return redirect(url_for("auth.login"))
        if not user.check_password(password):
            flash("Contraseña incorrecta", "danger")
            return redirect(url_for("auth.login"))
        session['user'] = user.email
        flash("Bienvenido", "success")
        return redirect(url_for("home"))
    
    return render_template("auth/login.html")

@bp.route('/logout')
def logout():
    if session.get('user'):
        del session['user']
        session.clear()
        flash("Hasta pronto", "success")
        
    else:
        flash("No has iniciado sesión", "danger")
    return redirect(url_for("home"))

