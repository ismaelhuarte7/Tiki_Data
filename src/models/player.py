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
        return '<Player %r>' % self.user_name
    
    def list():
        return Player.query.all()
    
    def create(name, surname, birth_date):
        player = Player(name=name, surname=surname, birth_date=birth_date)
        db.session.add(player)
        db.session.commit()
        return player
    
    def get_by_id(id):
        return Player.query.get(id)
    
    def update_profile_picture(id, profile_picture):
        player = Player.query.get(id)
        player.profile_picture = profile_picture
        db.session.commit()
        return player