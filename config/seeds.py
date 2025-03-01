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
    player4 = Player.create("Player", "Four", "2000-01-01")
    player5 = Player.create("Player", "Five", "2000-01-01")
    player6 = Player.create("Player", "Six", "2000-01-01")
    player7 = Player.create("Player", "Seven", "2000-01-01")
    player8 = Player.create("Player", "Eight", "2000-01-01")
    player9 = Player.create("Player", "Nine", "2000-01-01")
    player10 = Player.create("Player", "Ten", "2000-01-01")
    user4 = User.create("player4","player4@gmail.com","12345678",4)
    user5 = User.create("player5","player5@gmail.com","12345678",5)
    user6 = User.create("player6","player6@gmail.com","12345678",6)
    user7 = User.create("player7","player7@gmail.com","12345678",7)
    user8 = User.create("player8","player8@gmail.com","12345678",8)
    user9 = User.create("player9","player9@gmail.com","12345678",9)
    user10 = User.create("player10","player10@gmail.com","12345678",10)
    court1 = Court.create("Las palmas 27", "27 y 41")
    court2 = Court.create("Las palmas 22", "22 y 37")
    
