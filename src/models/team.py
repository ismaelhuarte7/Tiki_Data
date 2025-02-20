from config.database import db

player_team = db.Table('player_team',
    db.Column('player_id', db.Integer, db.ForeignKey('player.id'), primary_key=True),
    db.Column('team_id', db.Integer, db.ForeignKey('team.id'), primary_key=True)
)

class Team (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(80), nullable=False)
    id_match = db.Column(db.Integer, db.ForeignKey('match.id'), nullable=False)
    players = db.relationship('Player', secondary='player_team', back_populates='teams')
    
    def create(name, description, id_match):
        team = Team(name=name, description=description, id_match=id_match)
        db.session.add(team)
        db.session.commit()
        return team