from config.database import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    player_id = db.Column(db.Integer,db.ForeignKey('player.id'), nullable=True)
    is_verified = db.Column(db.Boolean, default=False)
    

    def __repr__(self):
        return f"<User {self.username}>"
    
    def get_all_users():
        return User.query.all()
    
    def create(username, email, password, player_id):
        passwordhash = generate_password_hash(password,"scrypt", 8)
        user = User(username=username, email=email, password=passwordhash, player_id=player_id)
        db.session.add(user)
        db.session.commit()
        return user
    
    def get_by_id(id):
        return User.query.get(id)
    
    def get_by_username(username):
        return User.query.filter_by(username=username).first()
    
    def get_by_email(email):
        return User.query.filter_by(email=email).first()
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def verify(self):
        self.is_verified = True
        db.session.commit()

    def get_by_player_id(player_id):
        return User.query.filter_by(player_id=player_id).first()
    

    