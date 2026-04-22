from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from src.models import Match, User, Court, Player, Team, Goal, GuestPlayer, News, Notification, MVPVote
from datetime import datetime
import json
from src.services.match_service import MatchService

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
    MatchService.finalize_expired_mvp_votes()

    match = Match.get_by_id(id)
    if not match:
        flash('Partido no encontrado', 'danger')
        return redirect(url_for('match.index'))
    
    user = None
    if 'user' in session:
        user = User.get_by_id(session['user']['id'])

    participant_ids = {player.id for player in match.players}
    voter_player_id = user.player_id if user else None
    vote = None
    if voter_player_id:
        vote = MVPVote.query.filter_by(match_id=match.id, voter_player_id=voter_player_id).first()

    is_participant = voter_player_id in participant_ids if voter_player_id else False
    can_vote = is_participant and match.is_mvp_voting_open() and vote is None
    voting_candidates = []
    if is_participant:
        voting_candidates = [p for p in match.players if p.id != voter_player_id]

    now = datetime.utcnow()
    voting_deadline = match.get_mvp_voting_deadline()
    voting_remaining_hours = max(0, int((voting_deadline - now).total_seconds() // 3600))
    
    return render_template(
        "match/show.html",
        match=match,
        user=user,
        can_vote=can_vote,
        has_voted=vote is not None,
        user_vote=vote,
        is_participant=is_participant,
        voting_candidates=voting_candidates,
        voting_deadline=voting_deadline,
        voting_remaining_hours=voting_remaining_hours
    )


@bp.route('/<int:id>/vote-mvp', methods=['POST'])
def vote_mvp(id):
    if 'user' not in session:
        flash('Debes iniciar sesión', 'danger')
        return redirect(url_for('auth.login'))

    user = User.get_by_id(session['user']['id'])
    if not user or not user.player_id:
        flash('No tenés un jugador asociado para votar', 'danger')
        return redirect(url_for('match.show', id=id))

    voted_player_id = request.form.get('voted_player_id', type=int)
    if not voted_player_id:
        flash('Debes seleccionar un jugador para votar', 'warning')
        return redirect(url_for('match.show', id=id))

    success, message = MatchService.register_mvp_vote(
        match_id=id,
        voter_player_id=user.player_id,
        voted_player_id=voted_player_id
    )

    flash(message, 'success' if success else 'danger')
    return redirect(url_for('match.show', id=id))

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