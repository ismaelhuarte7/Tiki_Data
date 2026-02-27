from config.database import db

class Goal (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(80), nullable=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=True)  # Puede ser null si es guest
    guest_player_id = db.Column(db.Integer, db.ForeignKey('guest_player.id'), nullable=True)  # Jugador invitado
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)  # Equipo que marcó
    match_id = db.Column(db.Integer, db.ForeignKey('match.id'), nullable=False)
    
    player = db.relationship('Player', backref='goals', foreign_keys=[player_id])
    guest_player = db.relationship('GuestPlayer', backref='goals', foreign_keys=[guest_player_id])
    team = db.relationship('Team', backref='goals')
    
    def __repr__(self):
        scorer = self.player.name if self.player else (self.guest_player.name if self.guest_player else 'Unknown')
        return f'<Goal by {scorer}>'
    
    @staticmethod
    def create(match_id, team_id, player_id=None, guest_player_id=None, goal_type=None):
        goal = Goal(
            match_id=match_id, 
            team_id=team_id,
            player_id=player_id, 
            guest_player_id=guest_player_id,
            type=goal_type
        )
        db.session.add(goal)
        db.session.commit()
        return goal
    
    def get_scorer_name(self):
        """Retorna el nombre del goleador (registrado o invitado)"""
        if self.player:
            return f"{self.player.name} {self.player.surname}"
        elif self.guest_player:
            return self.guest_player.name
        return "Desconocido"