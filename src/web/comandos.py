from config import database, seeds

def register(app):
    @app.cli.command("reset-db")
    def reset_db():
        database.reset()

    @app.cli.command("seed-db")
    def seed_db():
        seeds.run()
        print("Base de datos sembrada")