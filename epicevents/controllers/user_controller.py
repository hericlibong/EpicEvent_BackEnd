from dao.user_dao import UserDAO
from utils.security import hash_password, create_access_token, verify_password, verify_access_token


class UserController:
    def __init__(self):
        self.user_dao = UserDAO()

    def register_user(self, user_data):
        """
        Enregistrer un utilisateur avec les données fournies.
        """
        try:
        # Vérifier que l'utilisateur n'existe pas déjà
            existing_user = self.user_dao.get_user_by_username(user_data.get('username'))
            if existing_user:
                raise ValueError("Nom d'utilisateur déjà utilisé.")
            
        # Vérifier que l'adresse email n'est pas déjà utilisée
            existing_email = self.user_dao.get_user_by_email(user_data.get('email'))
            if existing_email:
                raise ValueError("Adresse email déjà utilisée.")
            

        # Vérifier que le départment est fourni
            if not user_data.get('department_id'):
                raise ValueError("Département non fourni.")
            
            # Hasher le mot de passe
            user_data['hashed_password'] = hash_password(user_data.pop('password'))

            # Créer l'utilisateur
            user = self.user_dao.create_user(user_data)
            #print(f"Utilisateur créé avec succès : {user.username}")
            return user
        except Exception as e:
            print(f"L'utilisateur n'a pas pu être créé: {e}")
            return None

    def login_user(self, username, password):
        """
        Authentifier un utilisateur et générer un token d'accès.
        """
        user = self.user_dao.get_user_by_username(username)
        if not user:
            # print("Utilisateur non trouvé.")
            return None, "Utilisateur non trouvé."
        
        if not verify_password(password, user.hashed_password):
            # print("Mot de passe incorrect.")
            return None, "Mot de passe incorrect."
        
        # Générer un token d'accès
        token_data = {
            'user_id': user.id,
            'username': user.username,
            'department': user.department.name,
        }
       #  print(f"Token data : {token_data}")
        token = create_access_token(token_data)
        # print(f"Utilisateur authentifié : {user.username}")
        return token, user
    
    def get_user(self, user_id):
        """
        Récupérer un utilisateur par son identifiant.
        """
        user = self.user_dao.get_user_by_id(user_id)
        if not user:
            print("Utilisateur non trouvé.")
            return
        return user
    
    def get_users_list(self):
        """
        Récupérer tous les utilisateurs.
        """
        users = self.user_dao.get_all_users()
        if not users:
            print("Aucun utilisateur trouvé.")
            return
        return users
    
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
    
    def delete_user(self, user_id):
        """
        Supprimer un utilisateur par son identifiant.
        """
        result = self.user_dao.delete_user(user_id)
        if not result:
            print("Utilisateur non trouvé.")
            return
        print("Utilisateur supprimé avec succès.")

    def verify_token(self, token):
        """
        Vérifier un token d'accès.
        """
        try:
            user_data = verify_access_token(token)
            return user_data
        except Exception as e:
            print(f"Erreur de vérification du token : {e}")
            return None
    
    
    def close(self):
        self.user_dao.close()

    

