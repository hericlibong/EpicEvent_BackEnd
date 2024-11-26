from models.user import User
from .base_dao import BaseDAO
from sqlalchemy.orm import joinedload

class UserDAO(BaseDAO):
    
    def create_user(self, user_data):
        """
        Créer un utilisateur avec les données fournies.
        """
        user = User(**user_data)
        self.session.add(user)
        self.session.commit()
        #self.session.refresh(user)

        # Recharger l'utilisateur avec les relations nécessaires
        user = self.session.query(User).options(
            joinedload(User.department)
        ).filter_by(id=user.id).one()

        # Détacher l'objet de la session
        self.session.expunge(user)
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
    
    # def get_all_users(self) -> list[User]:
    #     """
    #     Récupère tous les utilisateurs.
    #     """
    #     return self.session.query(User).all()

    def get_all_users(self):
        """
        Récupère tous les utilisateurs.
        """
        return self.session.query(User).options(
            joinedload(User.department)
        ).all()
    
    def get_user_by_email(self, email: str) -> User:
        """
        Récupère un utilisateur par son adresse email.
        """
        return self.session.query(User).filter_by(email=email).first()
    
    
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
