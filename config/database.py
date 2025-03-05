from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text 

db = SQLAlchemy()

def init_app(app):
    db.init_app(app)
    print("Base de datos inicializada")
    
    config(app)
    return app

def config(app):
    @app.teardown_appcontext
    def close_session(exception=None):
        db.session.close()
    return app

def reset():
    """
    Resetea la base de datos.
    """
    print("Eliminando la base de datos")
    db.reflect()
    db.drop_all()

    print("Creando la base de datos")
    with db.engine.connect() as connection:    
        print("Tablas existentes antes de crear:", connection.execute(text("SHOW TABLES")).fetchall())
    db.create_all()
    with db.engine.connect() as connection:
        print("Tablas existentes después de crear:", connection.execute(text("SHOW TABLES")).fetchall())
    print("Base de datos creada")