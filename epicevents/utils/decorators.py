# utils/decorators.py
import functools
import click
from controllers.user_controller import UserController
from utils.permissions import has_permission
import inspect  # Pour inspecter les arguments de la fonction (précision de l'argument 'user_data')

def require_permission(*permissions):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            controller = UserController()
            token = click.prompt('Veuillez entrer votre Token d\'accès')

            # Vérifier l'authentification
            user_data = controller.verify_token(token)
            if not user_data:
                click.echo("Token invalide ou expiré. Authentification échouée.")
                return

            # Vérifier les permissions en fonction du département de l'utilisateur
            user_department = user_data.get('department')
            user_permissions = [perm for perm in permissions if has_permission(user_department, perm)]
            if not user_permissions:
                click.echo("Vous n'avez pas la permission d'effectuer cette action.")
                return
            
            sig = inspect.signature(f)
            if 'user_permissions' in sig.parameters:
                return f(user_data, user_permissions, *args, **kwargs)
            else:
                return f(user_data, *args, **kwargs)
        return wrapper
    return decorator            

