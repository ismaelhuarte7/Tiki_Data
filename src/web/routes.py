from flask import Blueprint
from config.config import env
from config.database import db
from src.models.user import User  # Asegúrate de que esta es la ruta correcta para tu modelo User

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def home():
    users = User.query.all()
    users_list = "<br>".join([f"ID: {user.id}, Username: {user.username}, Email: {user.email}" for user in users])
    return f"¡Hola, Flask está funcionando! Entorno: {env}<br><br>{users_list}"
