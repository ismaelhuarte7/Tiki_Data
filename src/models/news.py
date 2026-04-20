from config.database import db

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=True)
    court_id = db.Column(db.Integer, db.ForeignKey('court.id'), nullable=True)
    match_id = db.Column(db.Integer, db.ForeignKey('match.id'), nullable=True)

    user = db.relationship('User', backref='news')
    player = db.relationship('Player', backref='news')
    court = db.relationship('Court', backref='news')
    match = db.relationship('Match', backref='news')

    @staticmethod
    def create(title, content, user_id, player_id=None, court_id=None, match_id=None):
        news = News(
            title=title,
            content=content,
            user_id=user_id,
            player_id=player_id,
            court_id=court_id,
            match_id=match_id
        )
        db.session.add(news)
        db.session.commit()
        return news

    @staticmethod
    def get_all():
        return News.query.order_by(News.created_at.desc()).all()