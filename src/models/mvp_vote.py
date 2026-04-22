from config.database import db
from datetime import datetime


class MVPVote(db.Model):
    __tablename__ = 'mvp_vote'

    id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, db.ForeignKey('match.id'), nullable=False, index=True)
    voter_player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False, index=True)
    voted_player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (
        db.UniqueConstraint('match_id', 'voter_player_id', name='uq_mvp_vote_match_voter'),
    )

    match = db.relationship('Match', backref=db.backref('mvp_votes', cascade='all, delete-orphan', lazy=True))
    voter = db.relationship('Player', foreign_keys=[voter_player_id], backref='mvp_votes_cast')
    voted_player = db.relationship('Player', foreign_keys=[voted_player_id], backref='mvp_votes_received')

    def __repr__(self):
        return f'<MVPVote match={self.match_id} voter={self.voter_player_id} voted={self.voted_player_id}>'
