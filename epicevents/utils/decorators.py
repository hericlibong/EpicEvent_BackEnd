# utils/decorators.py

from functools import wraps
from utils.security import verify_access_token
from utils.roles import UserRole

def requires_role(required_role):
    """
    Décorateur pour vérifier que l'utilisateur a le rôle requis.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Récupérer le token depuis les arguments ou le contexte
            token = kwargs.get('token')
            if not token:
                print("Token manquant.")
                return

            payload = verify_access_token(token)
            if not payload:
                print("Accès non autorisé : token invalide.")
                return

            user_role = payload.get('role')
            if user_role != required_role.value:
                print(f"Accès non autorisé : rôle {user_role} requis {required_role.value}.")
                return

            return f(*args, **kwargs)
        return decorated_function
    return decorator
