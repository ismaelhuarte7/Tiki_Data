from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from vercel_blob.blob_store import put
import uuid
import os
from src.models import Court, User, News

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
        News.create(
            title="Nueva Cancha Registrada",
            content=f"Se ha registrado una nueva cancha: {court.name}.",
            user_id=session['user']['id'],
            court_id=court.id
        )
        flash("Cancha creada correctamente", "success")
        return redirect(url_for('court.list'))

    return render_template("court/create.html")

@bp.route('/list')
def list():
    courts = Court.list()
    user = User.get_by_id(session['user']['id'])
    return render_template("court/list.html", courts=courts, user=user)


@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if 'user' not in session:
        flash("Debes iniciar sesión para editar una cancha", "danger")
        return redirect(url_for('auth.login'))
    user=User.get_by_id(session['user']['id'])
    if user.is_admin == False:
        flash("No tienes permiso para editar una cancha", "danger")
        return redirect(url_for('court.list'))

    court = Court.get_by_id(id)
    if request.method == "POST":
        name = request.form.get("name")
        address = request.form.get("address")
        picture = request.files.get("picture")

        if not name or not address:
            flash("Todos los campos son obligatorios", "danger")
            return render_template("court/edit.html", court=court)

        # Subir la imagen si se proporciona
        picture_url = None
        if picture and picture.filename != '':
            try:
                if court.picture:
                    response = delete(
                        url=court.picture,
                        options={"token": os.getenv("BLOB_READ_WRITE_TOKEN")}
                    )
                file_name = f"court_pictures/{uuid.uuid4()}_{picture.filename}"
                response = put(
                    path=file_name,
                    data=picture.read(),
                    options={"token": os.getenv("BLOB_READ_WRITE_TOKEN")}
                )
                picture_url = response.get("url")  # Obtener la URL del archivo subido
            except Exception as e:
                flash(f"Error al subir la imagen: {str(e)}", "danger")
                return render_template("court/edit.html", court=court)

        # Actualizar la cancha en la base de datos
        court = Court.update(id, name=name, address=address, picture=picture_url)
        flash("Cancha actualizada correctamente", "success")
        return redirect(url_for('court.list'))

    return render_template("court/edit.html", court=court)


@bp.route('delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    if 'user' not in session:
        flash("Debes iniciar sesión para eliminar una cancha", "danger")
        return render_template('auth/login')
    
    user=User.get_by_id(session['user']['id'])
    if user.is_admin == False:
        flash("No tienes permiso para eliminar una cancha", "danger")
        return render_template('court/list')
    
    try:
        court = Court.get_by_id(id)
        if court:
            if court.picture:
                response = delete(
                    url=court.picture,
                    options={"token": os.getenv("BLOB_READ_WRITE_TOKEN")}
                )
            Court.delete(id)
            flash("Cancha eliminada correctamente", "success")
        else:
            flash("Cancha no encontrada", "danger")
    except Exception as e:
        flash(f"Error al eliminar la cancha: {str(e)}", "danger")
        return render_template('court/list')
    court = Court.get_by_id(id)
    Court.delete(id)
    flash("Cancha eliminada correctamente", "success")
    return render_template('court/list')