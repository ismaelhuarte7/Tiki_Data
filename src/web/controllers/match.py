from flask import Blueprint, render_template, request, redirect, url_for, flash
from src.models import Match
from src.models import Court
from src.models import Player

bp = Blueprint("match", __name__, url_prefix="/match")

@bp.route('/', methods=['GET'])
def index():
    matches = Match.get_all_matches()
    return render_template("match/index.html", matches=matches)

@bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == "POST":
        date = request.form["match_date"]
        court_id = request.form["court_id"]
        match = Match.create(date, court_id)
        return redirect(url_for("match.create"))
    courts = Court.get_all_courts()
    players = Player.get_all_players()
    return render_template("match/create.html", courts=courts, players=players)


@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    match = Match.get_by_id(id)
    if request.method == "POST":
        date = request.form["date"]
        result = request.form["result"]
        court_id = request.form["court_id"]
        match.update(date, result, court_id)
        return redirect(url_for("match.index"))
    return render_template("match/edit.html", match=match)

@bp.route('/<int:id>/delete', methods=['GET'])
def delete(id):
    match = Match.get_by_id(id)
    match.delete()
    return redirect(url_for("match.index"))

