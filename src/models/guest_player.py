from config.database import db

# Tabla de relación entre jugadores invitados y partidos
guest_player_match = db.Table('guest_player_match',
    db.Column('guest_player_id', db.Integer, db.ForeignKey('guest_player.id'), primary_key=True),
    db.Column('match_id', db.Integer, db.ForeignKey('match.id'), primary_key=True),
    db.Column('team_id', db.Integer, db.ForeignKey('team.id'), nullable=True)
)

class GuestPlayer(db.Model):
    """Jugador invitado que no tiene cuenta en la plataforma"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    
    # Relación many-to-many con Match
    matches = db.relationship('Match', secondary='guest_player_match', back_populates='guest_players')
    
    def __repr__(self):
        return f'<GuestPlayer {self.name}>'
    
    @staticmethod
    def create(name):
        guest = GuestPlayer(name=name)
        db.session.add(guest)
        db.session.commit()
        return guest
    
    @staticmethod
    def get_by_id(id):
        return GuestPlayer.query.get(id)
