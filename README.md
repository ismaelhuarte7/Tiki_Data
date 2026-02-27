# Tiki - Sistema de Gestión Deportiva

## 🏃 Desarrollo Local

### Requisitos
- Python 3.8+
- MySQL
- Redis (opcional, usa filesystem si no está disponible)

### Configuración

1. **Activar entorno virtual:**
```powershell
.\vnev\Scripts\Activate.ps1
```

2. **Instalar dependencias:**
```powershell
pip install -r requirements.txt
```

3. **Configurar variables de entorno (.env):**
```env
FLASK_ENV=development
SECRET_KEY=tu-clave-secreta
db_user=root
db_password=tu_password
db_host=localhost
db_name=tiki_db
REDIS_URL=redis://localhost:6379  # Opcional
BASE_URL=http://localhost:5000
```

4. **Crear base de datos:**
```sql
CREATE DATABASE tiki_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

5. **Ejecutar:**
```powershell
python app.py
```

### Comandos Flask
```powershell
flask reset-db  # Resetear base de datos
flask seed-db   # Sembrar datos de prueba
```

---

## 🚀 Despliegue en Railway

### 1. Crear servicios en Railway:
- **MySQL** (Base de datos)
- **Redis** (Sesiones)  
- **Web Service** (La aplicación Flask)

### 2. Variables de entorno en Railway:

En tu servicio Web, configura:

```env
FLASK_ENV=production
SECRET_KEY=clave-secreta-segura-aleatoria
BASE_URL=https://tu-app.railway.app

# MySQL - Railway las proporciona automáticamente como:
# MYSQLUSER, MYSQLPASSWORD, MYSQLHOST, MYSQLDATABASE, MYSQLPORT
# Pero también puedes usar tus propias variables:
db_user=${{MySQL.MYSQLUSER}}
db_password=${{MySQL.MYSQLPASSWORD}}
db_host=${{MySQL.MYSQLHOST}}
db_name=${{MySQL.MYSQLDATABASE}}

# Redis - Railway las proporciona automáticamente
REDIS_URL=${{Redis.REDIS_URL}}

# Email (opcional)
MAILJET_API_KEY=tu_api_key
MAILJET_SECRET_KEY=tu_secret_key
MAIL_DEFAULT_SENDER=noreply@tudominio.com
```

### 3. Configurar Start Command:
```bash
gunicorn app:app
```

### 4. Instalar Gunicorn:
Agregar a `requirements.txt`:
```
gunicorn==21.2.0
```

---

## 📁 Estructura

```
├── app.py              # Punto de entrada
├── config/
│   ├── config.py       # Selector de configuración
│   ├── development.py  # Config desarrollo (local)
│   ├── production.py   # Config producción (Railway)
│   └── database.py     # Configuración de BD
├── src/
│   ├── models/         # Modelos de datos
│   └── web/
│       ├── controllers/  # Lógica de negocio
│       ├── templates/    # Vistas HTML
│       ├── static/       # CSS, JS
│       └── utils/
│           └── storage.py  # Almacenamiento local
└── uploads/            # Archivos subidos (imágenes)
```

---

## 🗄️ Almacenamiento

Las imágenes se guardan localmente en `/uploads/`:
- `uploads/player/` - Fotos de jugadores
- `uploads/court/` - Fotos de canchas
- `uploads/news/` - Imágenes de noticias

**Nota para Railway:** Considera usar un volumen persistente o migrar a un servicio de almacenamiento en la nube (S3, Cloudinary) en el futuro.

---

## 🔧 Stack Tecnológico

- **Framework:** Flask 3.1.0
- **Base de datos:** MySQL
- **Sesiones:** Redis
- **ORM:** SQLAlchemy
- **Email:** Mailjet (opcional)
