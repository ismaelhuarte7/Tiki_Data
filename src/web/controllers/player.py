
from flask import Blueprint, render_template, session, request, flash, redirect, url_for
from vercel_blob.blob_store import put, delete
import uuid
import os
from src.models import Player,User

bp = Blueprint("player", __name__, url_prefix="/player")

@bp.route('/list')
def list():
    players = Player.list()
    return render_template("player/list.html", players=players)

@bp.route('/show/<int:id>')
def show(id):
    player = Player.get_by_id(id)
    user = User.get_by_player_id(id)
    if not player:
        flash("Ese jugador no existe o fue eliminado", "danger")
        return render_template('home.html')
    return render_template("player/show.html", player=player, user=user)

@bp.route('/upload_profile_picture', methods=['GET', 'POST'])
def upload_profile_picture():
    if 'user' not in session:
        flash("Debes iniciar sesión para subir una foto de perfil", "danger")
        return redirect(url_for('auth.login'))
    
    if request.method == "POST":
        if 'profile_picture' not in request.files:
            flash("No se ha seleccionado ningún archivo", "danger")
            return redirect(url_for('player.show', id=session['user']['id']))

        file = request.files['profile_picture']
        if file.filename == '':
            flash("No se ha seleccionado ningún archivo", "danger")
            return redirect(url_for('player.show', id=session['user']['id']))
        
        user = User.get_by_id(session['user']['id'])
        player = Player.get_by_id(user.player_id)
        if user.player_id != player.id:
            flash("No tienes permiso para subir una foto de perfil", "danger")
            return redirect(url_for('player.show', id=session['user']['id']))
        

        # Genera un nombre único para el archivo
        file_name = f"profile_pictures/{uuid.uuid4()}_{file.filename}"

        try:
            if player.profile_picture:
                response = delete(
                    url=player.profile_picture,
                    options={"token": os.getenv("BLOB_READ_WRITE_TOKEN")}
                )
                pass
            response = put(
                path=file_name,
                data=file.read(),
                options={"token": os.getenv("BLOB_READ_WRITE_TOKEN")}
            )
            file_url = response.get("url")  # Obtén la URL del archivo subido

            # Guarda la URL en la base de datos
            user = User.get_by_id(session['user']['id'])
            Player.update_profile_picture(user.player_id, file_url)

            flash("Foto de perfil actualizada correctamente", "success")
        except Exception as e:
            flash(f"Error al subir la foto de perfil: {str(e)}", "danger")

    return redirect(url_for('player.show', id=session['user']['id']))

@bp.route('/delete_profile_picture', methods=['GET'])
def delete_profile_picture():
    if 'user' not in session:
        flash("Debes iniciar sesión para eliminar la foto de perfil", "danger")
        return redirect(url_for('auth.login'))
    user = User.get_by_id(session['user']['id'])
    player = Player.get_by_id(user.player_id)
    if user.player_id != player.id:
        flash("No tienes permiso para eliminar la foto de perfil", "danger")
        return redirect(url_for('player.show', id=session['user']['id']))

    try:
        user = User.get_by_id(session['user']['id'])
        player = Player.get_by_id(user.player_id)

        if player.profile_picture:
            response = delete(
                url=player.profile_picture,
                options={"token": os.getenv("BLOB_READ_WRITE_TOKEN")}
            )
            pass

        # Actualiza la base de datos
        Player.update_profile_picture(user.player_id, None)

        flash("Foto de perfil eliminada correctamente", "success")
    except Exception as e:
        flash(f"Error al eliminar la foto de perfil: {str(e)}", "danger")

    return redirect(url_for('player.show', id=session['user']['id']))

        
