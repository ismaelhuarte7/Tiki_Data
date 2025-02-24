from flask import Blueprint, render_template, request, redirect, url_for, flash
from src.models import Match

bp = Blueprint("match", __name__, url_prefix="/match")

@bp.route('/', methods=['GET'])
def index():
    matches = Match.get_all_matches()
    return render_template("match/index.html", matches=matches)

@bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == "POST":
        date = request.form["date"]
        result = request.form["result"]
        court_id = request.form["court_id"]
        match = Match.create(date, result, court_id)
        return redirect(url_for("match.index"))
    return render_template("match/create.html")