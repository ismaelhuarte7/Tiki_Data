from config.database import db

class Player (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    surname = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    user_name = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    birth_date = db.Column(db.DateTime, nullable=False)
    #rol_id = db.Column(db.Integer, db.ForeignKey('rol.id'), nullable=False)
    
    matches = db.relationship('Match', secondary='player_match', back_populates='players')
    teams = db.relationship('Team', secondary='player_team', back_populates='players')
    
    def __repr__(self):
        return '<Player %r>' % self.user_name
    
    def list():
        return Player.query.all()
    
    def create(name, surname, email, user_name, password, birth_date):
        player = Player(name=name, surname=surname, email=email, user_name=user_name, password=password, birth_date=birth_date)
        db.session.add(player)
        db.session.commit()
        return player
    
    def get_by_id(id):
        return Player.query.get(id)