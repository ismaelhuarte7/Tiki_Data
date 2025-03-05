from config.database import db

class Court (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(80), nullable=False)

    matches = db.relationship('Match', back_populates='court', lazy=True)
    
    def create(name, address):
        court = Court(name=name, address=address)
        db.session.add(court)
        db.session.commit()
        return court
    
    def get_all_courts():
        return Court.query.all()