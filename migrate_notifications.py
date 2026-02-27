"""
Script de migración para agregar tablas de notificaciones y actualizar noticias
"""

from app import app
from config.database import db
from sqlalchemy import text

def migrate():
    with app.app_context():
        try:
            print("Iniciando migración de notificaciones...")
            
            # 1. Crear tabla de notificaciones
            print("\n1. Creando tabla notification...")
            create_notification_table = """
            CREATE TABLE IF NOT EXISTS notification (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                message VARCHAR(255) NOT NULL,
                match_id INT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE,
                FOREIGN KEY (match_id) REFERENCES `match`(id) ON DELETE CASCADE,
                INDEX idx_user_id (user_id),
                INDEX idx_match_id (match_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
            """
            db.engine.connect().execute(text(create_notification_table))
            db.session.commit()
            print("✓ Tabla notification creada exitosamente")
            
            # 2. Agregar columna match_id a tabla news
            print("\n2. Agregando columna match_id a tabla news...")
            try:
                add_match_id_to_news = """
                ALTER TABLE news
                ADD COLUMN match_id INT NULL,
                ADD FOREIGN KEY (match_id) REFERENCES `match`(id) ON DELETE CASCADE;
                """
                db.engine.connect().execute(text(add_match_id_to_news))
                db.session.commit()
                print("✓ Columna match_id agregada a news")
            except Exception as e:
                if "Duplicate column name" in str(e):
                    print("⚠ Columna match_id ya existe en news")
                else:
                    raise e
            
            print("\n✅ Migración completada exitosamente!")
            print("\nResumen de cambios:")
            print("- Tabla 'notification' creada")
            print("- Columna 'match_id' agregada a tabla 'news'")
            
        except Exception as e:
            print(f"\n❌ Error durante la migración: {str(e)}")
            db.session.rollback()
            raise

if __name__ == "__main__":
    migrate()
