from models.user import User
from .base_dao import BaseDAO
from sqlalchemy.orm import joinedload
from utils.log_decorator import log_exceptions
from utils.logger import get_logger


class UserDAO(BaseDAO):
    def __init__(self):
        super().__init__() # Appeler le constructeur de la classe parente
        self.logger = get_logger('dao') # Récupérer un logger spécifique

    @log_exceptions('dao')
    def create_user(self, user_data):
        """
        Créer un utilisateur avec les données fournies.
        """
        self.logger.info("Creating user ...")
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
    
    @log_exceptions('dao')
    def get_user_by_username(self, username: str) -> User:
        """
        Récupère un utilisateur par son nom d'utilisateur.
        """
        self.logger.info(f"fetching user by username: {username}")
        return self.session.query(User).filter_by(username=username).first()
    
    @log_exceptions('dao')
    def get_user_by_id(self, user_id: int) -> User:
        """
        Récupère un utilisateur par son identifiant.
        """
        self.logger.info(f"fetching user by id: {user_id}")
        return self.session.query(User).filter_by(id=user_id).first()
    
    @log_exceptions('dao')
    def get_all_users(self):
        """
        Récupère tous les utilisateurs.
        """
        self.logger.info("fetching all users ...")
        return self.session.query(User).options(
            joinedload(User.department)
        ).all()
    
    @log_exceptions('dao')
    def get_user_by_email(self, email: str) -> User:
        """
        Récupère un utilisateur par son adresse email.
        """
        self.logger.info(f"fetching user by email: {email}")
        return self.session.query(User).filter_by(email=email).first()
    
    @log_exceptions('dao')
    def update_user(self, user_id: int, user_data: dict) -> User:
        """
        Met à jour un utilisateur avec les données fournies.
        """
        self.logger.info(f"updating user with id: {user_id}")
        user = self.get_user_by_id(user_id)
        if not user:
            return None
        for key, value in user_data.items():
            setattr(user, key, value)
        self.session.commit()
        # Recharger l'utilisateur avec les relations nécessaires
        user = self.session.query(User).options(
            joinedload(User.department)
        ).filter_by(id=user.id).one()

        # Détacher l'objet de la session
        self.session.expunge(user)
        return user
    
    @log_exceptions('dao')
    def delete_user(self, user_id: int) -> bool:
        self.logger.info(f"Deleting user ID: {user_id}")
        user = self.get_user_by_id(user_id)
        if not user:
            self.logger.warning(f"User ID {user_id} not found for deletion")
            return False
        self.session.delete(user)
        self.session.commit()
        return True
    
    
