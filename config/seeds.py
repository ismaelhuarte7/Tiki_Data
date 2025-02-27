from datetime import datetime
from src.models.user import User
from src.models.player import Player
from config.database import db

def run():
    # Crear 10 jugadores y sus respectivos usuarios
    for i in range(1, 11):
        # Crear el jugador
        player = Player.create(
            name=f"Player{i}",
            surname=f"Surname{i}",
            birth_date=datetime(1990 + i, i, i)  # Fecha de nacimiento ficticia
        )
        
        # Crear el usuario asociado al jugador
        user = User.create(
            username=f"user{i}",
            email=f"user{i}@example.com",
            password="password123",  # Contraseña común para todos los usuarios (en producción, usa contraseñas únicas)
            player_id=player.id
        )
        
        print(f"Usuario {user.username} creado con el jugador {player.name} {player.surname}")
