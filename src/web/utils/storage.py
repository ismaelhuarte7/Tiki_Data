"""
Utilidad para almacenamiento de archivos
Soporta Cloudinary y almacenamiento local como fallback
"""
import os
from werkzeug.utils import secure_filename
from flask import current_app
import uuid

# Importar Cloudinary con fallback
try:
    import cloudinary
    import cloudinary.uploader
    CLOUDINARY_AVAILABLE = True
except ImportError:
    CLOUDINARY_AVAILABLE = False


def _init_cloudinary():
    """Inicializa Cloudinary con las credenciales de la configuración"""
    if not CLOUDINARY_AVAILABLE:
        return False
    
    config = current_app.config
    if not config.get('USE_CLOUDINARY', False):
        return False
    
    cloudinary.config(
        cloud_name=config.get('CLOUDINARY_CLOUD_NAME'),
        api_key=config.get('CLOUDINARY_API_KEY'),
        api_secret=config.get('CLOUDINARY_API_SECRET'),
        secure=True
    )
    return True


def save_file(file, folder='general'):
    """
    Guarda un archivo en Cloudinary o en el sistema local
    
    Args:
        file: Archivo desde request.files
        folder: Subcarpeta/carpeta en Cloudinary (player, court, news, etc.)
    
    Returns:
        dict: {'url': 'url_completa', 'filename': 'nombre_archivo', 'public_id': 'id_cloudinary'}
    """
    if not file:
        return None
    
    # Intentar usar Cloudinary primero
    if _init_cloudinary():
        try:
            # Generar nombre único
            filename = secure_filename(file.filename)
            unique_name = f"{uuid.uuid4().hex}_{filename}"
            public_id = f"tiki/{folder}/{unique_name.rsplit('.', 1)[0]}"
            
            # Subir a Cloudinary
            result = cloudinary.uploader.upload(
                file,
                public_id=public_id,
                folder=f"tiki/{folder}",
                resource_type="auto",
                transformation=[
                    {'width': 1200, 'height': 1200, 'crop': 'limit'},
                    {'quality': 'auto:good'}
                ]
            )
            
            return {
                'url': result['secure_url'],
                'filename': unique_name,
                'public_id': result['public_id']
            }
        except Exception as e:
            print(f"Error subiendo a Cloudinary: {e}")
            # Continuar con almacenamiento local en caso de error
    
    # Fallback: Almacenamiento local
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


def delete_file(file_path_or_url):
    """
    Elimina un archivo de Cloudinary o del sistema local
    
    Args:
        file_path_or_url: URL de Cloudinary o ruta local del archivo
    """
    try:
        # Si es URL de Cloudinary
        if isinstance(file_path_or_url, str) and 'cloudinary.com' in file_path_or_url:
            if _init_cloudinary():
                # Extraer public_id de la URL
                # Formato: https://res.cloudinary.com/{cloud_name}/image/upload/v{version}/{public_id}.{ext}
                parts = file_path_or_url.split('/')
                if 'upload' in parts:
                    upload_idx = parts.index('upload')
                    # El public_id está después de upload/v{version}/
                    public_id_parts = parts[upload_idx + 2:]  # Saltar 'upload' y version
                    public_id = '/'.join(public_id_parts).rsplit('.', 1)[0]  # Remover extensión
                    
                    cloudinary.uploader.destroy(public_id)
                    return True
        
        # Fallback: Eliminar del sistema local
        file_path = file_path_or_url
        if file_path.startswith('/uploads/'):
            upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
            file_path = os.path.join(upload_folder, file_path.replace('/uploads/', ''))
        
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
            
    except Exception as e:
        print(f"Error eliminando archivo: {e}")
    
    return False


def get_file_url(path_or_url):
    """
    Convierte una ruta relativa en URL completa (solo para archivos locales)
    
    Args:
        path_or_url: Ruta relativa o URL completa
    
    Returns:
        str: URL completa del archivo
    """
    if not path_or_url:
        return None
    
    # Si ya es una URL completa (Cloudinary o http), retornar tal cual
    if path_or_url.startswith('http'):
        return path_or_url
    
    # Si es una ruta relativa local, agregar el dominio
    base_url = current_app.config.get('BASE_URL', 'http://localhost:5000')
    return f"{base_url}{path_or_url}"
