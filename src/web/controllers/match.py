from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from src.models import Match, User, Court, Player, Team, Goal, GuestPlayer, News, Notification
from datetime import datetime
import json

bp = Blueprint("match", __name__, url_prefix="/match")

@bp.route('/', methods=['GET'])
def index():
    page = request.args.get('page', 1, type=int)
    matches_pagination = Match.query.order_by(Match.date.desc()).paginate(
        page=page, per_page=5, error_out=False
    )
    user = None
    if 'user' in session:
        user = User.get_by_id(session['user']['id'])
    return render_template("match/index.html", matches_pagination=matches_pagination, user=user)

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
        match_date = datetime.strptime(request.form["match_date"], '%Y-%m-%d %H:%M')
        match_type = request.form["match_type"]
        court_id = request.form["court_id"]
        
        team_a_players = json.loads(request.form["team_a_players"])
        team_a_guests = json.loads(request.form["team_a_guests"])
        team_b_players = json.loads(request.form["team_b_players"])
        team_b_guests = json.loads(request.form["team_b_guests"])
        goals_data = json.loads(request.form["goals_data"])
        
        from src.services.match_service import MatchService
        match_id, error = MatchService.create_match(
            match_date=match_date,
            match_type=match_type,
            court_id=court_id,
            team_a_players=team_a_players,
            team_a_guests=team_a_guests,
            team_b_players=team_b_players,
            team_b_guests=team_b_guests,
            goals_data=goals_data,
            user_id=user.id
        )
        
        if error:
            flash(f"Error al crear el partido: {error}", "danger")
            return redirect(url_for('match.create'))
            
        flash('Partido creado exitosamente', 'success')
        return redirect(url_for('match.show', id=match_id))
    
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