from flask import Blueprint, session, render_template, request, redirect, url_for, flash
from src.models import Match
from src.models import Court
from src.models import Player
from src.models import Goal, User, News

bp = Blueprint("match", __name__, url_prefix="/match")

@bp.route('/list', methods=['GET'])
def list():
    matches = Match.get_all_matches()
    user = User.get_by_id(session['user']['id'])
    return render_template("match/list.html", matches=matches, user=user)

@bp.route('/create', methods=['GET', 'POST'])
def create():
    if 'user' not in session:
        flash("Debes iniciar sesión para registrar un partido", "danger")
        return redirect(url_for('auth.login'))
    user=User.get_by_id(session['user']['id'])
    if user.is_admin == False:
        flash("No tienes permiso para registrar un partido", "danger")
        return redirect(url_for('match.list'))
    if request.method == "POST":
        date = request.form["match_date"]
        court_id = request.form["court_id"]
        match_type = request.form["match_type"]  # Nuevo campo: tipo de partido
        
        match = Match.create(date, court_id, match_type)
        
        players_per_team = {
            "futbol_5": 5,
            "futbol_6": 6,
            "futbol_7": 7,
            "futbol_9": 9,
            "futbol_11": 11,
        }.get(match_type, 0)
        
        goals_team1 = 0
        goals_team2 = 0
        
        # Procesar los goles de los jugadores del Equipo 1
        for i in range(1, players_per_team + 1):
            player_id = request.form.get(f"player1_{i}")
            player = Player.get_by_id(player_id)
            match.add_player(player)
            goals = int(request.form.get(f"goals_player1_{i}"))
            goals_team1 += goals
            for _ in range(goals):
                Goal.create(player_id=player_id, match_id=match.id)
        
        # Procesar los goles de los jugadores del Equipo 2
        for i in range(1, players_per_team + 1):
            player_id = request.form.get(f"player2_{i}")
            player = Player.get_by_id(player_id)
            match.add_player(player)
            goals = int(request.form.get(f"goals_player2_{i}"))
            goals_team2 += goals
            for _ in range(goals):
                Goal.create(player_id=player_id, match_id=match.id)
        
        match.set_result(f"Equipo1 {goals_team1} - {goals_team2} Equipo2")
        
        News.create(
            title="Nuevo Partido Registrado",
            content=f"Se ha registrado un nuevo partido en la cancha {match.court.name}.",
            user_id=session['user']['id']
        )
        
        return redirect(url_for("match.list"))
    
    courts = Court.get_all_courts()
    players = Player.list()
    return render_template("match/create.html", courts=courts, players=players)


@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    if 'user' not in session:
        flash("Debes iniciar sesión para editar un partido", "danger")
        return redirect(url_for('auth.login'))
    user=User.get_by_id(session['user']['id'])
    if user.is_admin == False:
        flash("No tienes permiso para editar un partido", "danger")
        return redirect(url_for('match.list'))
    match = Match.get_by_id(id)
    if request.method == "POST":
        date = request.form["date"]
        result = request.form["result"]
        court_id = request.form["court_id"]
        match.update(date, result, court_id)
        return redirect(url_for("match.list"))
    return render_template("match/edit.html", match=match)

@bp.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    if 'user' not in session:
        flash("Debes iniciar sesión para eliminar un partido", "danger")
        return redirect(url_for('auth.login'))
    user=User.get_by_id(session['user']['id'])
    if user.is_admin == False:
        flash("No tienes permiso para eliminar un partido", "danger")
        return redirect(url_for('match.list'))
    match = Match.get_by_id(id)
    match.delete()
    return redirect(url_for("match.list"))

@bp.route('/<int:id>', methods=['GET'])
def show(id):
    match = Match.get_by_id(id)
    if not match:
        flash("Partido no encontrado", "error")
        return redirect(url_for("match.list"))
    return render_template("match/show.html", match=match)
