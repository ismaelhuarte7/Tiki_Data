
from flask import Blueprint, render_template, session, request, flash, redirect, url_for
from src.web.utils.storage import save_file, delete_file
import os
from datetime import date
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
        return render_template('player/list.html')
    return render_template("player/show.html", player=player, user=user, today=date.today())

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
        

        try:
            # Eliminar foto anterior si existe
            if player.profile_picture:
                delete_file(player.profile_picture)
            
            # Guardar nueva foto
            result = save_file(file, folder='player')
            if result:
                file_url = result['url']
                
                # Guarda la URL en la base de datos
                Player.update_profile_picture(user.player_id, file_url)
                flash("Foto de perfil actualizada correctamente", "success")
            else:
                flash("Error al guardar la imagen", "danger")
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
            delete_file(player.profile_picture)

        # Actualiza la base de datos
        Player.update_profile_picture(user.player_id, None)

        flash("Foto de perfil eliminada correctamente", "success")
    except Exception as e:
        flash(f"Error al eliminar la foto de perfil: {str(e)}", "danger")

    return redirect(url_for('player.show', id=session['user']['id']))
