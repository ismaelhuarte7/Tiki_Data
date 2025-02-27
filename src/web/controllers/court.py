from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from vercel_blob.blob_store import put
import uuid
import os
from src.models import Court, User

bp = Blueprint("court", __name__, url_prefix="/court")

@bp.route('/create', methods=['GET', 'POST'])
def create():
    if 'user' not in session:
        flash("Debes iniciar sesión para registrar una cancha", "danger")
        return redirect(url_for('auth.login'))
    user=User.get_by_id(session['user']['id'])
    if user.is_admin == False:
        flash("No tienes permiso para registrar una cancha", "danger")
        return redirect(url_for('court.list'))

    if request.method == "POST":
        name = request.form.get("name")
        address = request.form.get("address")
        picture = request.files.get("picture")

        if not name or not address:
            flash("Todos los campos son obligatorios", "danger")
            return render_template("court/create.html")

        # Subir la imagen si se proporciona
        picture_url = None
        if picture and picture.filename != '':
            try:
                # Generar un nombre único para el archivo
                file_name = f"court_pictures/{uuid.uuid4()}_{picture.filename}"
                response = put(
                    path=file_name,
                    data=picture.read(),
                    options={"token": os.getenv("BLOB_READ_WRITE_TOKEN")}
                )
                picture_url = response.get("url")  # Obtener la URL del archivo subido
            except Exception as e:
                flash(f"Error al subir la imagen: {str(e)}", "danger")
                return render_template("court/create.html")

        # Crear la cancha en la base de datos
        court = Court.create(name=name, address=address, picture=picture_url)
        flash("Cancha creada correctamente", "success")
        return redirect(url_for('court.list'))

    return render_template("court/create.html")

@bp.route('/list')
def list():
    courts = Court.list()
    user = User.get_by_id(session['user']['id'])
    print("user", user) 
    return render_template("court/list.html", courts=courts, user=user)