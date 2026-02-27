"""
Script de migración para actualizar la base de datos con las nuevas funcionalidades de partidos
Ejecutar una sola vez: python migrate_match_system.py
"""
from app import app
from config.database import db
from sqlalchemy import text

def migrate_match_system():
    with app.app_context():
        try:
            print("Iniciando migración del sistema de partidos...")
            
            with db.engine.connect() as connection:
                # 1. Crear tabla guest_player
                print("1. Creando tabla guest_player...")
                connection.execute(text("""
                    CREATE TABLE IF NOT EXISTS guest_player (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(80) NOT NULL
                    )
                """))
                connection.commit()
                
                # 2. Agregar campo match_type a Match
                print("2. Agregando campo match_type a match...")
                try:
                    connection.execute(text("""
                        ALTER TABLE `match` ADD COLUMN match_type VARCHAR(20) DEFAULT '11' NOT NULL
                    """))
                    connection.commit()
                except Exception as e:
                    if "Duplicate column" in str(e):
                        print("   Campo match_type ya existe")
                    else:
                        raise e
                
                # 3. Actualizar tabla team
                print("3. Actualizando tabla team...")
                try:
                    connection.execute(text("""
                        ALTER TABLE team 
                        ADD COLUMN team_name VARCHAR(10),
                        ADD COLUMN score INT DEFAULT 0,
                        CHANGE COLUMN id_match match_id INT
                    """))
                    connection.commit()
                except Exception as e:
                    if "Duplicate column" in str(e):
                        print("   Columnas de team ya actualizadas")
                    else:
                        raise e
                
                # 4. Actualizar player_match para incluir team_id
                print("4. Actualizando tabla player_match...")
                try:
                    connection.execute(text("""
                        ALTER TABLE player_match ADD COLUMN team_id INT,
                        ADD FOREIGN KEY (team_id) REFERENCES team(id)
                    """))
                    connection.commit()
                except Exception as e:
                    if "Duplicate column" in str(e):
                        print("   team_id ya existe en player_match")
                    else:
                        raise e
                
                # 5. Crear tabla guest_player_match
                print("5. Creando tabla guest_player_match...")
                connection.execute(text("""
                    CREATE TABLE IF NOT EXISTS guest_player_match (
                        guest_player_id INT NOT NULL,
                        match_id INT NOT NULL,
                        team_id INT,
                        PRIMARY KEY (guest_player_id, match_id),
                        FOREIGN KEY (guest_player_id) REFERENCES guest_player(id),
                        FOREIGN KEY (match_id) REFERENCES `match`(id),
                        FOREIGN KEY (team_id) REFERENCES team(id)
                    )
                """))
                connection.commit()
                
                # 6. Crear tabla guest_player_team
                print("6. Creando tabla guest_player_team...")
                connection.execute(text("""
                    CREATE TABLE IF NOT EXISTS guest_player_team (
                        guest_player_id INT NOT NULL,
                        team_id INT NOT NULL,
                        PRIMARY KEY (guest_player_id, team_id),
                        FOREIGN KEY (guest_player_id) REFERENCES guest_player(id),
                        FOREIGN KEY (team_id) REFERENCES team(id)
                    )
                """))
                connection.commit()
                
                # 7. Actualizar tabla goal
                print("7. Actualizando tabla goal...")
                try:
                    connection.execute(text("""
                        ALTER TABLE goal 
                        MODIFY COLUMN player_id INT NULL,
                        ADD COLUMN guest_player_id INT,
                        ADD COLUMN team_id INT,
                        ADD FOREIGN KEY (guest_player_id) REFERENCES guest_player(id),
                        ADD FOREIGN KEY (team_id) REFERENCES team(id)
                    """))
                    connection.commit()
                except Exception as e:
                    if "Duplicate column" in str(e):
                        print("   Columnas de goal ya actualizadas")
                    else:
                        raise e
                
            print("\n✓ Migración completada exitosamente!")
            print("  Ahora puedes crear partidos con la nueva funcionalidad")
            
        except Exception as e:
            print(f"\n✗ Error en la migración: {e}")
            print(f"  Tipo de error: {type(e).__name__}")

if __name__ == '__main__':
    migrate_match_system()
