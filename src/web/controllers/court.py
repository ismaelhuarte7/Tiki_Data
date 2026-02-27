from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from src.web.utils.storage import save_file, delete_file
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
                # Guardar la imagen localmente
                result = save_file(picture, folder='court')
                if result:
                    picture_url = result['url']
                else:
                    flash("Error al guardar la imagen", "danger")
                    return render_template("court/create.html")
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
    user = None
    if 'user' in session:
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
                # Eliminar imagen anterior si existe
                if court.picture:
                    delete_file(court.picture)
                
                # Guardar nueva imagen
                result = save_file(picture, folder='court')
                if result:
                    picture_url = result['url']
                else:
                    flash("Error al guardar la imagen", "danger")
                    return render_template("court/edit.html", court=court)
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
        return render_template('auth/login.html')
    
    user=User.get_by_id(session['user']['id'])
    if user.is_admin == False:
        flash("No tienes permiso para eliminar una cancha", "danger")
        return render_template('court/list.html')
    
    try:
        court = Court.get_by_id(id)
        if court:
            # Eliminar imagen si existe
            if court.picture:
                delete_file(court.picture)
            
            Court.delete(id)
            flash("Cancha eliminada correctamente", "success")
        else:
            flash("Cancha no encontrada", "danger")
    except Exception as e:
        flash(f"Error al eliminar la cancha: {str(e)}", "danger")
        return render_template('court/list.html')
    
    return redirect(url_for('court.list'))