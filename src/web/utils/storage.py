"""
Utilidad para almacenamiento de archivos
Reemplaza Vercel Blob para desarrollo local
"""
import os
from werkzeug.utils import secure_filename
from flask import current_app, url_for
import uuid


def save_file(file, folder='general'):
    """
    Guarda un archivo en el sistema local
    
    Args:
        file: Archivo desde request.files
        folder: Subcarpeta dentro de uploads (player, court, news, etc.)
    
    Returns:
        dict: {'url': 'ruta_relativa', 'filename': 'nombre_archivo'}
    """
    if not file:
        return None
    
    # Crear directorio si no existe
    upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
    folder_path = os.path.join(upload_folder, folder)
    os.makedirs(folder_path, exist_ok=True)
    
    # Generar nombre único
    filename = secure_filename(file.filename)
    unique_filename = f"{uuid.uuid4().hex}_{filename}"
    
    # Guardar archivo
    file_path = os.path.join(folder_path, unique_filename)
    file.save(file_path)
    
    # Retornar URL relativa
    relative_path = f"/uploads/{folder}/{unique_filename}"
    
    return {
        'url': relative_path,
        'filename': unique_filename,
        'path': file_path
    }


def delete_file(file_path):
    """
    Elimina un archivo del sistema local
    
    Args:
        file_path: Ruta del archivo a eliminar (puede ser relativa o absoluta)
    """
    try:
        # Si es una URL relativa, convertir a ruta absoluta
        if file_path.startswith('/uploads/'):
            upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
            file_path = os.path.join(upload_folder, file_path.replace('/uploads/', ''))
        
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
    except Exception as e:
        print(f"Error eliminando archivo: {e}")
    
    return False


def get_file_url(relative_path):
    """
    Convierte una ruta relativa en URL completa
    
    Args:
        relative_path: Ruta relativa del archivo (ej: /uploads/player/imagen.jpg)
    
    Returns:
        str: URL completa del archivo
    """
    if not relative_path:
        return None
    
    # Si ya tiene el dominio, retornar tal cual
    if relative_path.startswith('http'):
        return relative_path
    
    # Si es una ruta relativa, agregar el dominio
    base_url = current_app.config.get('BASE_URL', 'http://localhost:5000')
    return f"{base_url}{relative_path}"
