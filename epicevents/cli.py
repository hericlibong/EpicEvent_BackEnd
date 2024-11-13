import click
from controllers.user_controller import UserController
#from sqlalchemy.orm import Session
from models import Role, Department  # Adjust the import path as necessary
from config import SessionLocal

from utils.roles import UserRole

@click.group()
def cli():
    pass

@cli.command()
def create_user():
    """
    Enregistrer un utilisateur avec les données fournies.
    """
    # Demander les informations de l'utilisateur
    username = click.prompt('Nom d\'utilisateur')
    password = click.prompt('Mot de passe', hide_input=True, confirmation_prompt=True)
    fullname = click.prompt('Nom complet', default='')
    email = click.prompt('Adresse email', default='')
    phone = click.prompt('Numéro de téléphone', default='')

    # Créer une session de base de données
    session = SessionLocal()

    try:
        # Sélection du rôle
        roles = session.query(Role).all()
        if not roles:
            click.echo("Aucun rôle disponible. Veuillez ajouter des rôles à la base de données.")
            session.close()
            return

        role_choices = {str(role.id): role.name for role in roles}
        click.echo('Rôles disponibles :')
        for role_id, role_name in role_choices.items():
            click.echo(f"{role_id}. {role_name}")
        role_id = click.prompt('Sélectionnez un rôle', type=click.Choice(role_choices.keys()))

        # Sélection du département
        departments = session.query(Department).all()
        if not departments:
            click.echo("Aucun département disponible. Veuillez ajouter des départements à la base de données.")
            session.close()
            return

        dept_choices = {str(dept.id): dept.name for dept in departments}
        click.echo('Départements disponibles :')
        for dept_id, dept_name in dept_choices.items():
            click.echo(f"{dept_id}. {dept_name}")
        department_id = click.prompt('Sélectionnez un département', type=click.Choice(dept_choices.keys()))

        # Préparer les données de l'utilisateur
        user_data = {
            'username': username,
            'password': password,
            'fullname': fullname,
            'email': email,
            'phone': phone,
            'role_id': int(role_id),
            'department_id': int(department_id),
        }

        # Enregistrer l'utilisateur via le contrôleur
        controller = UserController()
        try:
            user = controller.register_user(user_data)
            if user:
                click.echo(f"Utilisateur créé avec succès : {user.username}")
            else:
                click.echo("Erreur lors de la création de l'utilisateur.")
        except ValueError as e:
            click.echo(f"Erreur : {e}")
        finally:
            controller.close()
    finally:
        session.close()



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
