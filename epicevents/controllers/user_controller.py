from dao.user_dao import UserDAO
from utils.security import hash_password, create_access_token, verify_password, verify_access_token
from utils.logger import get_logger, log_error

class UserController:
    def __init__(self):
        self.user_dao = UserDAO()
        self.logger = get_logger('controller')

    def register_user(self, user_data):
        """
        Enregistrer un utilisateur avec les données fournies.
        Erreurs métier (ValueError) si :
        - Nom d'utilisateur déjà utilisé
        - Email non fourni
        - Email déjà utilisé
        - Département non fourni
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

        try:
            user = self.user_dao.create_user(user_data)
            return user
        except Exception as e:
            # Erreur inattendue (ex: problème BD)
            log_error(self.logger, "Erreur inattendue lors de la création de l'utilisateur", exception=e)
            raise Exception("Erreur lors de la création de l'utilisateur") from e

    def login_user(self, username, password):
        """
        Authentifier un utilisateur et générer un token d'accès.
        Erreur métier gérée en renvoyant None, message d'erreur simple pour la vue.
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
    
    def get_user(self, user_id):
        """
        Récupérer un utilisateur par son identifiant.
        Erreur métier si utilisateur introuvable.
        """
        user = self.user_dao.get_user_by_id(user_id)
        if not user:
            raise ValueError("Utilisateur non trouvé.")
        return user
    
    def get_users_list(self):
        """
        Récupérer tous les utilisateurs.
        Retourne une liste vide s'il n'y a pas d'utilisateurs.
        """
        users = self.user_dao.get_all_users()
        if not users:
            # Pas d'erreur métier, juste aucun utilisateur.
            return []
        return users
    
    def update_user(self, user_id, user_data):
        """
        Mettre à jour un utilisateur avec les données fournies.
        Erreur métier si utilisateur introuvable.
        """
        try:
            user = self.user_dao.update_user(user_id, user_data)
            if not user:
                raise ValueError("Utilisateur non trouvé.")
            return user
        except ValueError:
            # Erreur métier remontée telle quelle à la vue
            raise
        except Exception as e:
            # Erreur inattendue
            log_error(self.logger, "Erreur inattendue lors de la mise à jour de l'utilisateur", exception=e)
            raise Exception("Erreur lors de la mise à jour de l'utilisateur") from e
    
    def delete_user(self, user_id):
        """
        Supprimer un utilisateur par son identifiant.
        Renvoie True si succès, False si utilisateur introuvable.
        """
        try:
            result = self.user_dao.delete_user(user_id)
            if not result:
                raise ValueError("Utilisateur introuvable.")
            return True
        except ValueError:
            raise
        except Exception as e:
            # Erreur inattendue
            log_error(self.logger, "Erreur inattendue lors de la suppression de l'utilisateur", exception=e)
            raise Exception("Erreur lors de la suppression de l'utilisateur") from e

    def verify_token(self, token):
        """
        Vérifier un token d'accès.
        S'il y a une erreur inattendue ou d'autre problème, la vue le gérera.
        """
        try:
            user_data = verify_access_token(token)
            return user_data
        except Exception as e:
            # Par exemple si le token est invalide, on peut lever ValueError
            # ou retourner None. A vous de décider.
            # Ici on considère qu'un token invalide n'est pas une erreur inattendue
            # mais une erreur métier (ValueError).
            raise ValueError("Token invalide.") from e

    def close(self):
        self.user_dao.close()
