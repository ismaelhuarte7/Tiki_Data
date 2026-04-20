from config.database import db

class Court (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    address = db.Column(db.Text, nullable=False)  # Cambiado a Text para URLs largas de Google Maps
    picture = db.Column(db.String(255), nullable=True)


    def __repr__(self):
        return self.name
    
    @staticmethod
    def create(name, address, picture):
        court = Court(name=name, address=address, picture=picture)
        db.session.add(court)
        db.session.commit()
        return court
    
    @staticmethod
    def get_by_id(id):
        return Court.query.get(id)
    
    @staticmethod
    def list():
        return Court.query.all()
    
    @staticmethod
    def update(id, name, address, picture):
        court = Court.get_by_id(id)
        court.name = name
        court.address = address
        court.picture = picture
        db.session.commit()
        return court
    
    @staticmethod
    def delete(id):
        court = Court.get_by_id(id)
        db.session.delete(court)
        db.session.commit()
        return True
    
    