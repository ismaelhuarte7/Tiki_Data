"""
Script para corregir la tabla team eliminando columnas antiguas
Ejecutar una sola vez: python fix_team_table.py
"""
from app import app
from config.database import db
from sqlalchemy import text

def fix_team_table():
    with app.app_context():
        try:
            print("Corrigiendo estructura de la tabla team...")
            
            with db.engine.connect() as connection:
                # 1. Eliminar columnas antiguas name y description
                print("1. Eliminando columna 'name'...")
                try:
                    connection.execute(text("ALTER TABLE team DROP COLUMN name"))
                    connection.commit()
                    print("   ✓ Columna 'name' eliminada")
                except Exception as e:
                    if "Can't DROP" in str(e):
                        print("   - Columna 'name' ya fue eliminada")
                    else:
                        raise e
                
                print("2. Eliminando columna 'description'...")
                try:
                    connection.execute(text("ALTER TABLE team DROP COLUMN description"))
                    connection.commit()
                    print("   ✓ Columna 'description' eliminada")
                except Exception as e:
                    if "Can't DROP" in str(e):
                        print("   - Columna 'description' ya fue eliminada")
                    else:
                        raise e
                
                # 2. Hacer team_name NOT NULL
                print("3. Actualizando team_name a NOT NULL...")
                try:
                    connection.execute(text("ALTER TABLE team MODIFY COLUMN team_name VARCHAR(10) NOT NULL"))
                    connection.commit()
                    print("   ✓ team_name ahora es NOT NULL")
                except Exception as e:
                    print(f"   - Error al modificar team_name: {e}")
                
                # 3. Hacer match_id NOT NULL con foreign key
                print("4. Actualizando match_id a NOT NULL...")
                try:
                    connection.execute(text("ALTER TABLE team MODIFY COLUMN match_id INT NOT NULL"))
                    connection.commit()
                    print("   ✓ match_id ahora es NOT NULL")
                except Exception as e:
                    print(f"   - Error al modificar match_id: {e}")
            
            print("\n✓ Corrección completada exitosamente!")
            print("  Ahora puedes crear partidos sin errores")
            
        except Exception as e:
            print(f"\n✗ Error en la corrección: {e}")
            print(f"  Tipo de error: {type(e).__name__}")

if __name__ == '__main__':
    fix_team_table()
