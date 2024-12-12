# utils/decorators.py
import functools
import click
import sentry_sdk
from controllers.user_controller import UserController
from utils.permissions import has_permission
import inspect  # Pour inspecter les arguments de la fonction (précision de l'argument 'user_data')


# Décorateur pour vérifier les permissions de l'utilisateur
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
                # Journalisation de l'échec d'authentification
                sentry_sdk.capture_message(
                    "Tentative d'accès avec un token invalide ou expiré.",
                    level='warning'
                    )
                return

            # Vérifier les permissions en fonction du département de l'utilisateur
            user_department = user_data.get('department')
            user_permissions = [perm for perm in permissions if has_permission(user_department, perm)]
            if not user_permissions:
                click.echo("Vous n'avez pas la permission d'effectuer cette action.")
                # Journalisation de la tentative d'accès non autorisée
                sentry_sdk.capture_message(
                    f"Tentative d'accès non autorisée : utilisateur {user_data.get('username')}."
                    f"(Département : {user_department}), permission requise : {permissions}",
                    level='warning'
                    )
                return

            sig = inspect.signature(f)
            if 'user_permissions' in sig.parameters:
                return f(user_data, user_permissions, *args, **kwargs)
            else:
                return f(user_data, *args, **kwargs)
        return wrapper
    return decorator
