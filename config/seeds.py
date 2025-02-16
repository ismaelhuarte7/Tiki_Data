from src.models.user import User

def run():
    user1 = User.create_user(username="admin", email="email@gmail.com")
