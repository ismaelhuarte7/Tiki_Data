from config.database import db

class Player (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    surname = db.Column(db.String(80), nullable=False)
    birth_date = db.Column(db.DateTime, nullable=False)
    profile_picture = db.Column(db.String(255), nullable=True)
    
    matches = db.relationship('Match', secondary='player_match', back_populates='players')
    teams = db.relationship('Team', secondary='player_team', back_populates='players')
    user = db.relationship('User', back_populates='player', uselist=False)
    
    def __repr__(self):
        return f'<Player {self.name} {self.surname}>'
    
    @staticmethod
    def list():
        return Player.query.all()
    
    @staticmethod
    def create(name, surname, birth_date):
        player = Player(name=name, surname=surname, birth_date=birth_date)
        db.session.add(player)
        db.session.commit()
        return player
    
    @staticmethod
    def get_by_id(id):
        return Player.query.get(id)
    
    @staticmethod
    def update_profile_picture(id, profile_picture):
        player = Player.query.get(id)
        player.profile_picture = profile_picture
        db.session.commit()
        return player