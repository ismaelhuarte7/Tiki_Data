from flask import Blueprint, render_template, request, redirect, url_for, flash
from itsdangerous import URLSafeTimedSerializer
from flask import session, current_app
from flask_mail import Message
from datetime import datetime
from src.models import User, Player, News
from src.web import mail

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
            return render_template("auth/sign_up.html", 
                                 email=email, 
                                 username=username, 
                                 first_name=name, 
                                 last_name=surname, 
                                 birthdate=birth_date)
        
        if User.get_by_username(username):
            flash("El nombre de usuario ya está en uso.", "danger")
            return render_template("auth/sign_up.html", 
                                 email=email, 
                                 username=username, 
                                 first_name=name, 
                                 last_name=surname, 
                                 birthdate=birth_date)
        player = Player.create(name, surname, birth_date)
        user = User.create(username, email, password, player.id)
        
        if current_app.config.get('REQUIRE_EMAIL_VERIFICATION', False):
            flash("Te enviamos un correo para verificar tu cuenta, revisa tu casilla de SPAM", "info")
            send_verification_email(email)
            return render_template("auth/login.html")
        else:
            user.verify()
            session['user'] = {
                'id': user.id,       
                'email': user.email,     
                'username': user.username,
                'player_id': user.player_id
            }
            News.create(
                title="Nuevo Jugador Registrado",
                content=f"Bienvenido a Tiki-Data, {user.username}!",
                user_id=user.id,
                player_id=player.id
            )
            flash("Registro exitoso. Bienvenido!", "success")
            return redirect(url_for("home"))
        
    return render_template("auth/sign_up.html")

@bp.route('/login', methods=['GET', 'POST'])
def login():
    session.clear()
    if request.method == "POST":
        identifier = request.form["username"]  
        password = request.form["password"]

        if "@" in identifier:
            user = User.get_by_email(identifier)  
        else:
            user = User.get_by_username(identifier)
        if not user:
            flash("Usuario no encontrado", "danger")
            return render_template("auth/login.html")
        if not user.check_password(password):
            flash("Contraseña incorrecta", "danger")
            return render_template("auth/login.html")
        if current_app.config.get('REQUIRE_EMAIL_VERIFICATION', False) and not user.is_verified:
            flash("Usuario no verificado", "danger")
            return render_template("auth/login.html")
        session['user'] = {
            'id': user.id,       
            'email': user.email,     
            'username': user.username,
            'player_id': user.player_id
        }
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



def send_verification_email(to_email):
    """Envía email de verificación usando SMTP (Gmail)"""
    token = generate_verification_token(to_email)
    verification_url = f"{current_app.config['BASE_URL']}/auth/verify/{token}"
    user = User.get_by_email(to_email)

    # Renderizar plantilla HTML
    html_content = render_template(
        "auth/mail_verification.html", 
        mail_link_validator=verification_url, 
        username=user.username,
        current_year=datetime.now().year
    )

    try:
        if not current_app.config.get('MAIL_USERNAME') or not current_app.config.get('MAIL_PASSWORD'):
            current_app.logger.error("MAIL_USERNAME/MAIL_PASSWORD no configurados")
            return False

        message = Message(
            subject="Verifica tu cuenta - Tiki-Data",
            sender=current_app.config.get('MAIL_DEFAULT_SENDER') or current_app.config.get('MAIL_USERNAME'),
            recipients=[to_email],
            html=html_content,
        )
        mail.send(message)
        current_app.logger.info("Email de verificacion enviado a %s", to_email)
        return True
        
    except Exception as e:
        current_app.logger.exception("Error al enviar email de verificacion: %s", str(e))
        return False

def generate_verification_token(email):
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    return serializer.dumps(email, salt="email-confirm")
 

def confirm_verification_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt="email-confirm", max_age=expiration)
    except Exception:
        return None
    return email

@bp.route('/verify/<token>')
def verify(token):
    email = confirm_verification_token(token)
    if not email:
        flash("El enlace de verificación es inválido o ha expirado", "danger")
        return render_template("auth/login.html")
    user = User.get_by_email(email)
    user.verify()
    player = Player.get_by_id(user.player_id)
    News.create(
            title="Nuevo Jugador Registrado",
            content=f"Bienvenido a Tiki-Data, {user.username}!",
            user_id=user.id,
            player_id=player.id
        )
    session['user'] = {
        'id': user.id,       
        'email': user.email,     
        'username': user.username,
        'player_id': user.player_id
    }
    flash("Usuario verificado correctamente. Bienvenido!", "success")
    return redirect(url_for("home"))

    