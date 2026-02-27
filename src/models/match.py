from config.database import db

player_match = db.Table('player_match',
    db.Column('player_id', db.Integer, db.ForeignKey('player.id'), primary_key=True),
    db.Column('match_id', db.Integer, db.ForeignKey('match.id'), primary_key=True),
    db.Column('team_id', db.Integer, db.ForeignKey('team.id'), nullable=True)
)


class Match (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    match_type = db.Column(db.String(20), nullable=False)  # '5', '6', '7', '8', '11'
    result = db.Column(db.String(80), nullable=True)  # Formato: "3-2"
    court_id = db.Column(db.Integer, db.ForeignKey('court.id'), nullable=False)
    court = db.relationship('Court', backref='matches', lazy=True)
    players = db.relationship('Player', secondary='player_match', back_populates='matches')
    guest_players = db.relationship('GuestPlayer', secondary='guest_player_match', back_populates='matches')
    goals = db.relationship('Goal', backref='match', lazy=True, cascade='all, delete-orphan')
    teams = db.relationship('Team', backref='match', lazy=True, cascade='all, delete-orphan')
    mvp_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=True)
    mvp = db.relationship('Player', foreign_keys=[mvp_id], backref='mvp_matches', lazy=True)
    
    def __repr__(self):
        return f'<Match {self.id} - {self.result}>'
    
    @staticmethod
    def create(date, match_type, court_id, result=None):
        match = Match(date=date, match_type=match_type, result=result, court_id=court_id)
        db.session.add(match)
        db.session.commit()
        return match

    @staticmethod
    def get_all_matches():
        return Match.query.order_by(Match.date.desc()).all()
    
    @staticmethod
    def get_by_id(id):
        return Match.query.get(id)
    
    def get_team_a(self):
        """Obtiene el equipo A del partido"""
        for team in self.teams:
            if team.team_name == 'A':
                return team
        return None
    
    def get_team_b(self):
        """Obtiene el equipo B del partido"""
        for team in self.teams:
            if team.team_name == 'B':
                return team
        return None
    
    def get_max_players_per_team(self):
        """Retorna el número máximo de jugadores por equipo según el tipo"""
        match_types = {'5': 5, '6': 6, '7': 7, '8': 8, '11': 11}
        return match_types.get(self.match_type, 11)