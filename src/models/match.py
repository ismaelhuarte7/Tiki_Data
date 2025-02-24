from config.database import db

player_match = db.Table('player_match',
    db.Column('player_id', db.Integer, db.ForeignKey('player.id'), primary_key=True),
    db.Column('match_id', db.Integer, db.ForeignKey('match.id'), primary_key=True)
)


class Match (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    result = db.Column(db.String(80), nullable=True)
    court_id = db.Column(db.Integer, db.ForeignKey('court.id'), nullable=False)
    players = db.relationship('Player', secondary='player_match', back_populates='matches')
    goals = db.relationship('Goal', backref='match', lazy=True)
    mvp_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=True)
    
    
    
    def create(date, result, court_id):
        match = Match(date=date, result=result, court_id=court_id)
        db.session.add(match)
        db.session.commit()
        return match

    def get_all_matches():
        return Match.query.all()