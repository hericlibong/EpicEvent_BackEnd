import click
from controllers.user_controller import UserController
from utils.roles import UserRole

@click.group()
def cli():
    pass

@cli.command()
@click.option('--username', prompt='Nom d\'utilisateur')
@click.option('--password', prompt='Mot de passe', hide_input=True, confirmation_prompt=True)
@click.option('--role', prompt='Rôle', type=click.Choice(['Gestionnaire', 'Commercial', 'Support']))
def create_user(username, password, role):
    user_data = {
        'username': username,
        'password': password,
        'role': UserRole(role)
    }
    controller = UserController()
    controller.register_user(user_data)
    controller.close()

@cli.command()
@click.option('--username', prompt='Nom d\'utilisateur', help='Nom d\'utilisateur')
@click.option('--password', prompt='Mot de passe', hide_input=True, help='Mot de passe pour la connexion')
def login(username, password):
    """
    Authentifier un utilisateur et générer un token d'accès.
    """
    controller = UserController()
    token = controller.login_user(username, password)
    controller.close()
    if token:
        print(f"Token d'accès généré : {token}")
    else:
        print("Authentification échouée.")

if __name__ == '__main__':
    cli()
