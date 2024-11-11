from models.user import User
from config import SessionLocal

class UserDAO:
    def __init__(self):
        self.session = SessionLocal()
 
    def create_user(self, user_data):
        """
        Créer un utilisateur avec les données fournies.
        """
        user = User(**user_data)
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user
    
    def get_user_by_username(self, username: str) -> User:
        """
        Récupère un utilisateur par son nom d'utilisateur.
        """
        return self.session.query(User).filter_by(username=username).first()
    
    def get_user_by_id(self, user_id: int) -> User:
        """
        Récupère un utilisateur par son identifiant.
        """
        return self.session.query(User).filter_by(id=user_id).first()
    
    def get_all_users(self) -> list[User]:
        """
        Récupère tous les utilisateurs.
        """
        return self.session.query(User).all()
    
    def update_user(self, user_id: int, user_data: dict) -> User:
        """
        Met à jour un utilisateur avec les données fournies.
        """
        user = self.get_user_by_id(user_id)
        if not user:
            return None
        for key, value in user_data.items():
            setattr(user, key, value)
        self.session.commit()
        self.session.refresh(user)
        return user
    
    def delete_user(self, user_id: int) -> bool:
        """
        Supprime un utilisateur par son identifiant.
        """
        user = self.get_user_by_id(user_id)
        if not user:
            return False
        self.session.delete(user)
        self.session.commit()
        return True
    
    def close(self):
        self.session.close()