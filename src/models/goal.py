from config.database import db

class Goal (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(80), nullable=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    match_id = db.Column(db.Integer, db.ForeignKey('match.id'), nullable=False)
    
    def create(player_id, match_id):
        goal = Goal(player_id=player_id, match_id=match_id)
        db.session.add(goal)
        db.session.commit()
        return goal