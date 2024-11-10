from dao.user_dao import UserDAO
from utils.security import hash_password, create_access_token, verify_password
from utils.roles import UserRole

class UserController:
    def __init__(self):
        self.user_dao = UserDAO()

    def register_user(self, user_data):
        """
        Enregistrer un utilisateur avec les données fournies.
        """
        # Vérifier que l'utilisateur n'existe pas déjà
        existing_user = self.user_dao.get_user_by_username(user_data.get('username'))
        if existing_user:
            print("Cet utilisateur existe déjà.")
            return
        
        # Hasher le mot de passe
        user_data['hashed_password'] = hash_password(user_data.pop('password'))

        # Créer l'utilisateur
        user = self.user_dao.create_user(user_data)
        print(f"Utilisateur créé avec succès : {user.username}")

    def login_user(self, username, password):
        """
        Authentifier un utilisateur et générer un token d'accès.
        """
        user = self.user_dao.get_user_by_username(username)
        if not user:
            print("Utilisateur non trouvé.")
            return
        
        if not verify_password(password, user.hashed_password):
            print("Mot de passe incorrect.")
            return
        
        # Générer un token d'accès
        token_data = {
            'user_id': user.id,
            'username': user.username,
            'role': user.role.value,
        }
        token = create_access_token(token_data)
        print(f"Utilisateur authentifié : {user.username}")
        return token
    
    def close(self):
        self.user_dao.close()

    

