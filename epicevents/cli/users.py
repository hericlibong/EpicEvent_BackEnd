import click
from controllers.user_controller import UserController
from models import Department
from config import SessionLocal
from rich.table import Table
from rich.console import Console
from utils.decorators import require_permission

@click.group()
def users():
    """Commandes pour gérer les utilisateurs."""
    pass

@users.command(name='list-users')
@require_permission('can_list_users')
def list(user_data):
    """
    Lister tous les utilisateurs.
    """
    controller = UserController()
    users = controller.get_users_list()
    controller.close()

    if not users:
        click.echo("Aucun utilisateur trouvé.")
        return

    console = Console()
    table = Table(title="[bold cyan]Liste des utilisateurs[/]",
                  show_header=True,
                  show_lines=True,
                  header_style="bold magenta")
    table.add_column("ID", style="dim")
    table.add_column("Nom d'utilisateur")
    table.add_column("Nom complet")
    table.add_column("Email")
    table.add_column("Téléphone")
    table.add_column("Département")

    for user in users:
        table.add_row(
            str(user.id),
            user.username,
            user.fullname,
            user.email,
            user.phone,
            user.department.name
        )
    console.print(table)
   

@users.command()
@require_permission('can_manage_users')
def create(user_data):
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
            'department_id': int(department_id),
        }

        # Enregistrer l'utilisateur via le contrôleur
        controller = UserController()
        try:
            user = controller.register_user(user_data) # Vérifier l'argument de la fonction
            if user:
                click.echo(f"Utilisateur créé avec succès : {user.username}")
                console = Console()
                table = Table(title="Utilisateur créé avec succès", show_header=False)
                table.add_column("champ", style="bold cyan")
                table.add_column("valeur", style="bold magenta")
                table.add_row("ID", str(user.id))
                table.add_row("Nom d'utilisateur", user.username)
                table.add_row("Nom complet", user.fullname) 
                table.add_row("Email", user.email)
                table.add_row("Téléphone", user.phone)
                table.add_row("Département", user.department.name)
                console.print(table)
            else:
                click.echo("Erreur lors de la création de l'utilisateur.")
        except ValueError as e:
            click.echo(f"Erreur : {e}")
        finally:
            controller.close()
    finally:
        session.close()

@users.command()
@require_permission('can_manage_users')
def delete():
    """
    Supprimer un utilisateur avec l'ID fourni.
    """
    user_id = click.prompt('ID de l\'utilisateur à supprimer', type=int)

    controller = UserController()
    success = controller.delete_user(user_id)
    controller.close()

    if success:
        click.echo(f"Utilisateur ID {user_id} supprimé avec succès.")
    else:
        click.echo("Erreur lors de la suppression de l'utilisateur.")



@users.command()
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
        print("Copiez et collez le token pour accéder aux autres commandes.")
    else:
        print("Authentification échouée.")