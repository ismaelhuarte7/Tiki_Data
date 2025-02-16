from config.database import db

class Court (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(80), nullable=False)
    
    def create(name, address):
        court = Court(name=name, address=address)
        db.session.add(court)
        db.session.commit()
        return court