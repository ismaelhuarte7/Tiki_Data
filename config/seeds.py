from src.models.user import User
from src.models.player import Player
from src.models.court import Court

def run():
    playerTobi = Player.create("Tobias", "Napoli", "2003-10-16")
    user1 = User.create("tobinapoli","tobiasnapoli03@gmail.com","12345678",1)
    court1 = Court.create("Las palmas 27", "27 y 41")
    court2 = Court.create("Las palmas 22", "22 y 37")
    
