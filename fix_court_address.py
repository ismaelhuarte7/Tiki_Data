"""
Script para actualizar la columna 'address' de la tabla 'court' a TEXT
Ejecutar este script una sola vez para migrar la base de datos
"""
from app import app
from config.database import db
from sqlalchemy import text

def migrate_court_address():
    with app.app_context():
        try:
            # Modificar la columna address para permitir texto más largo (URLs de Google Maps)
            with db.engine.connect() as connection:
                connection.execute(text("ALTER TABLE court MODIFY COLUMN address TEXT NOT NULL"))
                connection.commit()
            print("✓ Migración exitosa: columna 'address' actualizada a TEXT")
            print("  Ahora puedes guardar URLs largas de Google Maps")
        except Exception as e:
            print(f"✗ Error en la migración: {e}")
            print("  Si el error dice que la columna ya es TEXT, la migración ya se aplicó.")

if __name__ == '__main__':
    migrate_court_address()
