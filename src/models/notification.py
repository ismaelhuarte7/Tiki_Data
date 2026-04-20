from config.database import db
from datetime import datetime, timezone

class Notification(db.Model):
    __tablename__ = 'notification'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    match_id = db.Column(db.Integer, db.ForeignKey('match.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    is_read = db.Column(db.Boolean, default=False)
    
    # Relaciones
    user = db.relationship('User', backref=db.backref('notifications', cascade='all, delete-orphan'))
    match = db.relationship('Match', backref='notifications')
    
    @staticmethod
    def create(user_id, message, match_id=None):
        """Crear una notificación para un usuario"""
        notification = Notification(
            user_id=user_id,
            message=message,
            match_id=match_id
        )
        db.session.add(notification)
        db.session.commit()
        return notification
    
    @staticmethod
    def get_by_user(user_id):
        """Obtener todas las notificaciones de un usuario"""
        return Notification.query.filter_by(user_id=user_id, is_read=False).order_by(Notification.created_at.desc()).all()
    
    @staticmethod
    def mark_as_read(notification_id):
        """Marcar como leída (actualizar is_read en la BD)"""
        notification = Notification.query.get(notification_id)
        if notification:
            notification.is_read = True
            db.session.commit()
            return True
        return False
    
    @staticmethod
    def count_by_user(user_id):
        """Contar notificaciones de un usuario"""
        return Notification.query.filter_by(user_id=user_id, is_read=False).count()
