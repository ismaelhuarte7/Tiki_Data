from flask import Blueprint, render_template, request, redirect, url_for, flash
from itsdangerous import URLSafeTimedSerializer
from flask import session, current_app
from flask import current_app
from mailjet_rest import Client
from src.models import User, Player

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route('/sign_up', methods=['GET', 'POST'])
def signup():
    session.clear()
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
        flash("Te enviamos un correo para verificar tu cuenta, revisa tu casilla de SPAM", "info")
        send_verification_email(email)
        
        return render_template("auth/login.html")
        
    return render_template("auth/sign_up.html")

@bp.route('/login', methods=['GET', 'POST'])
def login():
    session.clear()
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = User.get_by_email(email)
        if not user:
            flash("Usuario no encontrado", "danger")
            return render_template("auth/login.html")
        if not user.check_password(password):
            flash("Contraseña incorrecta", "danger")
            return render_template("auth/login.html")
        if not user.is_verified:
            flash("Usuario no verificado", "danger")
            return render_template("auth/login.html")
        session['user'] = {
            'id': user.id,       
            'email': user.email,     
            'username': user.username  
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
    token = generate_verification_token(to_email)
    verification_url = f"{current_app.config['BASE_URL']}/auth/verify/{token}"

    user = User.get_by_email(to_email)

    html_content = render_template("auth/mail_verification.html", mail_link_validator=verification_url, username=user.username)

    correo = {
        'Messages': [
            {
                "From": {
                    "Email": current_app.config.get('MAIL_DEFAULT_SENDER'),  
                    "Name": "Tiki-Data" 
                },
                "To": [
                    {
                        "Email": to_email,  
                        "Name": user.username 
                    }
                ],
                "Subject": "Verifica tu cuenta - Tiki-Data", 
                "TextPart": f"Por favor, verifica tu correo electrónico: {verification_url}",  
                "HTMLPart": html_content  
            }
        ]
    }

    try:
        mailjet = Client(auth=(current_app.config.get('MAILJET_API_KEY'), current_app.config.get('MAILJET_SECRET_KEY')), version='v3.1')
        resultado = mailjet.send.create(data=correo)
        if resultado.status_code == 200:
            print("Correo enviado correctamente")
        else:
            print("Error al enviar el correo:", resultado.json())
    except Exception as e:
        print("Error inesperado:", str(e))

def generate_verification_token(email):
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    return serializer.dumps(email, salt="email-confirm")
 

def confirm_verification_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt="email-confirm", max_age=expiration)
    except:
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
    flash("Usuario verificado correctamente", "success")
    return render_template("auth/login.html")

    