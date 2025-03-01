from src.models.user import User
from src.models.player import Player
from src.models.court import Court

def run():
    playerTobi = Player.create("Tobias", "Napoli", "2003-10-16")
    playerCanela = Player.create("Tobias", "Pena", "2004-03-03")
    playerCalvo = Player.create("Mariano", "Ortega", "2003-09-5")
    user1 = User.create("tobinapoli","tobiasnapoli03@gmail.com","12345678",1)
    user2 = User.create("canela","canela@gmail.com","12345678",2)
    user3 = User.create("calvo","calvo@gmail.com","12345678",3)
    court1 = Court.create("Las palmas 27", "27 y 41")
    court2 = Court.create("Las palmas 22", "22 y 37")
    
