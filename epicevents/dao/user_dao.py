from models.user import User
from config import SessionLocal

class UserDAO:
    def __init__(self):
        self.session = SessionLocal()

    def get_user_by_username(self, username: str) -> User:
        """
        Récupère un utilisateur par son nom d'utilisateur.
        """
        return self.session.query(User).filter_by(username=username).first()

        

    
    def create_user(self, user_data):
        """
        Créer un utilisateur avec les données fournies.
        """
        user = User(**user_data)
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user
    
    def close(self):
        self.session.close()