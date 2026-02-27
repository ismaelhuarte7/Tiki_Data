from config.database import db

player_team = db.Table('player_team',
    db.Column('player_id', db.Integer, db.ForeignKey('player.id'), primary_key=True),
    db.Column('team_id', db.Integer, db.ForeignKey('team.id'), primary_key=True)
)

guest_player_team = db.Table('guest_player_team',
    db.Column('guest_player_id', db.Integer, db.ForeignKey('guest_player.id'), primary_key=True),
    db.Column('team_id', db.Integer, db.ForeignKey('team.id'), primary_key=True)
)

class Team (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(10), nullable=False)  # 'A' o 'B'
    score = db.Column(db.Integer, default=0, nullable=False)
    match_id = db.Column(db.Integer, db.ForeignKey('match.id'), nullable=False)
    players = db.relationship('Player', secondary='player_team', back_populates='teams')
    guest_players = db.relationship('GuestPlayer', secondary='guest_player_team', backref='teams')
    
    def __repr__(self):
        return f'<Team {self.team_name} - Match {self.match_id}>'
    
    @staticmethod
    def create(team_name, match_id, score=0):
        team = Team(team_name=team_name, match_id=match_id, score=score)
        db.session.add(team)
        db.session.commit()
        return team
    
    @staticmethod
    def get_by_id(id):
        return Team.query.get(id)
    
    def add_player(self, player):
        """Agrega un jugador registrado al equipo"""
        if player not in self.players:
            self.players.append(player)
            db.session.commit()
    
    def add_guest_player(self, guest_player):
        """Agrega un jugador invitado al equipo"""
        if guest_player not in self.guest_players:
            self.guest_players.append(guest_player)
            db.session.commit()
    
    def get_all_players(self):
        """Retorna todos los jugadores (registrados e invitados)"""
        return {
            'registered': self.players,
            'guests': self.guest_players
        }