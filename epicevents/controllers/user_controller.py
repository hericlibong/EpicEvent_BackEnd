from dao.user_dao import UserDAO
from utils.security import hash_password, create_access_token, verify_password, verify_access_token
from utils.log_decorator import log_exceptions
from utils.logger import get_logger

class UserController:
    def __init__(self):
        self.user_dao = UserDAO()
        self.logger = get_logger('controller')

    @log_exceptions('controller')
    def register_user(self, user_data):
        """
        Enregistrer un utilisateur avec les données fournies.
        """
        # Vérifier que l'utilisateur n'existe pas déjà
        existing_user = self.user_dao.get_user_by_username(user_data.get('username'))
        if existing_user:
            raise ValueError("Nom d'utilisateur déjà utilisé.")

        # Vérifier que l'adresse email est fournie
        if not user_data.get('email'):
            raise ValueError("Adresse email non fournie.")

        # Vérifier que l'adresse email n'est pas déjà utilisée
        existing_email = self.user_dao.get_user_by_email(user_data.get('email'))
        if existing_email:
            raise ValueError("Adresse email déjà utilisée.")

        # Vérifier que le département est fourni
        if not user_data.get('department_id'):
            raise ValueError("Département non fourni.")

        # Hasher le mot de passe
        user_data['hashed_password'] = hash_password(user_data.pop('password'))

        user = self.user_dao.create_user(user_data)
        return user
         
    @log_exceptions('controller')
    def login_user(self, username, password):
        """
        Authentifier un utilisateur et générer un token d'accès.
        """
        user = self.user_dao.get_user_by_username(username)
        if not user:
            return None, "Utilisateur non trouvé."
        
        if not verify_password(password, user.hashed_password):
            return None, "Mot de passe incorrect."
        
        # Générer un token d'accès
        token_data = {
            'user_id': user.id,
            'username': user.username,
            'department': user.department.name,
        }
        token = create_access_token(token_data)
        return token, user
    
    @log_exceptions('controller')
    def get_user(self, user_id):
        """
        Récupérer un utilisateur par son identifiant.
        """
        user = self.user_dao.get_user_by_id(user_id)
        if not user:
            print("Utilisateur non trouvé.")
            return
        return user
    
    @log_exceptions('controller')
    def get_users_list(self):
        """
        Récupérer tous les utilisateurs.
        """
        users = self.user_dao.get_all_users()
        if not users:
            print("Aucun utilisateur trouvé.")
            return []
        return users
    
    @log_exceptions('controller')
    def update_user(self, user_id, user_data):
        """
        Mettre à jour un utilisateur avec les données fournies.
        """
        user = self.user_dao.update_user(user_id, user_data)
        if not user:
            print("Utilisateur non trouvé.")
            return
        print(f"Utilisateur mis à jour : {user.username}")
        return user
    
    @log_exceptions('controller')
    def delete_user(self, user_id):
        """
        Supprimer un utilisateur par son identifiant.
        """
        result = self.user_dao.delete_user(user_id)
        return result # Retourner expliccitement True ou False

    @log_exceptions('controller')
    def verify_token(self, token):
        """
        Vérifier un token d'accès.
        """
        user_data = verify_access_token(token)
        return user_data
        
    # déclancher une exception intentionnellement pour tester Sentry    
    @log_exceptions('controller')
    def trigger_exception(self):
        """Méthode pour déclencher une exception intentionnellement."""
        raise RuntimeError("Erreur intentionnelle pour tester Sentry.")
    
    # Déclencher une exception ValueError pour tester Sentry
    @log_exceptions('controller')
    def trigger_value_error(self):
        """Méthode pour déclencher une exception ValueError intentionnellement."""
        raise ValueError("Erreur de valeur intentionnelle pour tester Sentry.")
    
    # Déclencher une exception KeyError pour tester Sentry
    @log_exceptions('controller')
    def trigger_key_error(self):
        """Méthode pour déclencher une exception KeyError intentionnellement."""
        raise KeyError("Erreur de clé intentionnelle pour tester Sentry.")
    
    # Déclencher une exception TypeError pour tester Sentry
    @log_exceptions('controller')
    def trigger_type_error(self):
        """Méthode pour déclencher une exception TypeError intentionnellement."""
        raise TypeError("Erreur de type intentionnelle pour tester Sentry.")

    # Déclencher une exception IOError / OSError pour tester Sentry
    @log_exceptions('controller')
    def trigger_io_error(self):
        """Méthode pour déclencher une exception IOError intentionnellement."""
        raise IOError("Erreur d'entrée/sortie intentionnelle pour tester Sentry.")
    # Déclencher une exception AttributeError pour tester Sentry
    @log_exceptions('controller')
    def trigger_attribute_error(self):
        """Méthode pour déclencher une exception AttributeError intentionnellement."""
        raise AttributeError("Erreur d'attribut intentionnelle pour tester Sentry.")

    # Dclencher une exception IndexError pour tester Sentry
    @log_exceptions('controller')
    def trigger_index_error(self):
        """Méthode pour déclencher une exception IndexError intentionnellement."""
        raise IndexError("Erreur d'index intentionnelle pour tester Sentry.")
    
    def close(self):
        self.user_dao.close()
