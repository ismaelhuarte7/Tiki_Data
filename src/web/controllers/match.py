from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from src.models import Match, User, Court, Player, Team, Goal, GuestPlayer
from datetime import datetime
import json

bp = Blueprint("match", __name__, url_prefix="/match")

@bp.route('/', methods=['GET'])
def index():
    matches = Match.get_all_matches()
    user = None
    if 'user' in session:
        user = User.get_by_id(session['user']['id'])
    return render_template("match/index.html", matches=matches, user=user)

@bp.route('/create', methods=['GET', 'POST'])
def create():
    # Verificar que el usuario sea admin
    if 'user' not in session:
        flash('Debes iniciar sesión', 'danger')
        return redirect(url_for('auth.login'))
    
    user = User.get_by_id(session['user']['id'])
    if not user.is_admin:
        flash('No tienes permisos para crear partidos', 'danger')
        return redirect(url_for('match.index'))
    
    if request.method == "POST":
        try:
            # 1. Obtener datos básicos
            match_date = datetime.strptime(request.form["match_date"], '%Y-%m-%d %H:%M')
            match_type = request.form["match_type"]
            court_id = request.form["court_id"]
            
            # 2. Parsear datos de los equipos
            team_a_players = json.loads(request.form["team_a_players"])  # Lista de IDs
            team_a_guests = json.loads(request.form["team_a_guests"])    # Lista de nombres
            team_b_players = json.loads(request.form["team_b_players"])
            team_b_guests = json.loads(request.form["team_b_guests"])
            
            # 3. Parsear datos de goles
            goals_data = json.loads(request.form["goals_data"])
            
            # 4. Calcular resultado
            score_a = len([g for g in goals_data if g['team'] == 'A'])
            score_b = len([g for g in goals_data if g['team'] == 'B'])
            result = f"{score_a}-{score_b}"
            
            # 5. Crear el partido
            match = Match.create(date=match_date, match_type=match_type, court_id=court_id, result=result)
            
            # 6. Crear equipos
            team_a = Team.create(team_name='A', match_id=match.id, score=score_a)
            team_b = Team.create(team_name='B', match_id=match.id, score=score_b)
            
            # 7. Agregar jugadores registrados a Equipo A
            for player_id in team_a_players:
                player = Player.get_by_id(int(player_id))
                if player:
                    team_a.add_player(player)
                    # Agregar jugador también a la relación con el partido
                    if player not in match.players:
                        match.players.append(player)
            
            # 8. Agregar jugadores invitados a Equipo A
            for guest_name in team_a_guests:
                guest = GuestPlayer.create(name=guest_name)
                team_a.add_guest_player(guest)
                # Agregar invitado también a la relación con el partido
                if guest not in match.guest_players:
                    match.guest_players.append(guest)
            
            # 9. Agregar jugadores registrados a Equipo B
            for player_id in team_b_players:
                player = Player.get_by_id(int(player_id))
                if player:
                    team_b.add_player(player)
                    # Agregar jugador también a la relación con el partido
                    if player not in match.players:
                        match.players.append(player)
            
            # 10. Agregar jugadores invitados a Equipo B
            for guest_name in team_b_guests:
                guest = GuestPlayer.create(name=guest_name)
                team_b.add_guest_player(guest)
                # Agregar invitado también a la relación con el partido
                if guest not in match.guest_players:
                    match.guest_players.append(guest)
            
            # Guardar las relaciones jugador-partido
            from config.database import db
            db.session.commit()
            
            # 11. Registrar goles
            for goal_data in goals_data:
                team = team_a if goal_data['team'] == 'A' else team_b
                
                if goal_data['scorer_type'] == 'player':
                    # Gol de jugador registrado
                    Goal.create(
                        match_id=match.id,
                        team_id=team.id,
                        player_id=int(goal_data['scorer_id'])
                    )
                else:
                    # Gol de jugador invitado - buscar el guest player por nombre
                    guest_name = goal_data['scorer_name']
                    guest_players = team_a.guest_players if goal_data['team'] == 'A' else team_b.guest_players
                    guest = next((g for g in guest_players if g.name == guest_name), None)
                    
                    if guest:
                        Goal.create(
                            match_id=match.id,
                            team_id=team.id,
                            guest_player_id=guest.id
                        )
            
            flash('Partido registrado exitosamente', 'success')
            return redirect(url_for('match.show', id=match.id))
            
        except Exception as e:
            flash(f'Error al registrar el partido: {str(e)}', 'danger')
            return redirect(url_for('match.create'))
    
    # GET - Mostrar formulario
    courts = Court.list()
    players = Player.list()
    return render_template("match/create.html", courts=courts, players=players, user=user)

@bp.route('/<int:id>', methods=['GET'])
def show(id):
    match = Match.get_by_id(id)
    if not match:
        flash('Partido no encontrado', 'danger')
        return redirect(url_for('match.index'))
    
    user = None
    if 'user' in session:
        user = User.get_by_id(session['user']['id'])
    
    return render_template("match/show.html", match=match, user=user)

@bp.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    # Verificar que el usuario sea admin
    if 'user' not in session:
        flash('Debes iniciar sesión', 'danger')
        return redirect(url_for('auth.login'))
    
    user = User.get_by_id(session['user']['id'])
    if not user.is_admin:
        flash('No tienes permisos para eliminar partidos', 'danger')
        return redirect(url_for('match.index'))
    
    match = Match.get_by_id(id)
    if not match:
        flash('Partido no encontrado', 'danger')
        return redirect(url_for('match.index'))
    
    try:
        from config.database import db
        db.session.delete(match)
        db.session.commit()
        flash('Partido eliminado exitosamente', 'success')
    except Exception as e:
        flash(f'Error al eliminar el partido: {str(e)}', 'danger')
    
    return redirect(url_for('match.index'))