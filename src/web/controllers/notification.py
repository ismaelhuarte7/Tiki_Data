from flask import Blueprint, request, jsonify, session
from src.models import Notification, User

bp = Blueprint("notification", __name__, url_prefix="/notification")

@bp.route('/mark-read/<int:id>', methods=['POST'])
def mark_read(id):
    """Marcar notificación como leída (eliminarla)"""
    if 'user' not in session:
        return jsonify({'success': False, 'message': 'No autorizado'}), 401
    
    user_id = session['user']['id']
    notification = Notification.query.get(id)
    
    # Verificar que la notificación pertenece al usuario
    if not notification or notification.user_id != user_id:
        return jsonify({'success': False, 'message': 'Notificación no encontrada'}), 404
    
    Notification.mark_as_read(id)
    
    return jsonify({
        'success': True,
        'message': 'Notificación marcada como leída',
        'remaining': Notification.count_by_user(user_id)
    })

@bp.route('/get-all', methods=['GET'])
def get_all():
    """Obtener todas las notificaciones del usuario actual"""
    if 'user' not in session:
        return jsonify({'success': False, 'message': 'No autorizado'}), 401
    
    user_id = session['user']['id']
    notifications = Notification.get_by_user(user_id)
    
    return jsonify({
        'success': True,
        'notifications': [{
            'id': n.id,
            'message': n.message,
            'match_id': n.match_id,
            'created_at': n.created_at.strftime('%d/%m/%Y %H:%M')
        } for n in notifications],
        'count': len(notifications)
    })
