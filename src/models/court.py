from config.database import db

class Court (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    picture = db.Column(db.String(255), nullable=True)

    
    def create(name, address, picture):
        court = Court(name=name, address=address, picture=picture)
        db.session.add(court)
        db.session.commit()
        return court
    
    def get_by_id(id):
        return Court.query.get(id)
    
    def list():
        return Court.query.all()