import click
import sentry_sdk
from controllers.user_controller import UserController
from models import Department
from config import SessionLocal
from rich.table import Table
from rich.console import Console
from utils.decorators import require_permission
from utils.logger import log_info, log_error, get_logger

logger = get_logger('users')

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
    try:
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
        log_info(
            logger,
            "Liste des utilisateurs affichée avec succès."
        )
        
        return "Success"
        
    except Exception as e:
        # Capture de l'exception avec Sentry
        log_error(
            logger,
            "Erreur lors de l'affichage de la liste des utilisateurs",
            exception=e
        )
        
        click.echo("Une erreur inattendue est survenue.")
        return e

   
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
                # Journaliser la création de l'utilisateur
                log_info(
                    logger,
                    f"Utilisateur créé avec succès : {user.username}",
                    user_id=user.id,
                    department = user.department.name
                )
                
                # sentry_sdk.capture_message(f"Utilisateur créé : {user.username}", level="info")
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
        except Exception as e:   
            
            # Capture des erreurs inattendues
            log_error(
                logger,
                "Erreur lors de la création de l'utilisateur",
                exception=e
            )
            # sentry_sdk.capture_exception(e)
            click.echo(f"Erreur : {e}")
        finally:
            controller.close()
    finally:
        session.close()

@users.command()
@require_permission('can_manage_users')
def delete(user_data):
    """
    Supprimer un utilisateur avec l'ID fourni.
    """
    user_id = click.prompt('ID de l\'utilisateur à supprimer', type=int)
    try:
        controller = UserController()
        success = controller.delete_user(user_id)
        controller.close()

        if success:
            log_info(
                logger,
                f"Utilisateur ID {user_id} : supprimé avec succès."
            )
            click.echo(f"Utilisateur ID {user_id} : supprimé avec succès.")
        
        else:
            click.echo(f"Erreur : Utilisateur ID {user_id} introuvable ou non supprime*é.")
    except Exception as e:
        # Capture de l'exception avec Sentry
        log_error(
            logger,
            "Erreur lors de la suppression de l'utilisateur",
            exception=e
        )
        click.echo(f"Erreur inattendue : {e}")



@users.command()
@click.option('--username', prompt='Nom d\'utilisateur', help='Nom d\'utilisateur')
@click.option('--password', prompt='Mot de passe', hide_input=True, help='Mot de passe pour la connexion')
def login(username, password):
    """
    Authentifier un utilisateur et générer un token d'accès.
    """
    try:
        controller = UserController()
        token, result = controller.login_user(username, password)
        controller.close()
        
        if token:
            log_info(
                logger,
                f"Authentification réussie : {username}",
                user_id=result.id,
                department=result.department.name

            )
            user = result  # L'objet utilisateur
            console = Console()
            table = Table(title="Authentification réussie !!", show_header=False)
            table.add_column("Champ", style="bold cyan")
            table.add_column("Valeur", style="bold magenta")
            table.add_row("ID utilisateur", str(user.id))
            table.add_row("Nom d'utilisateur", user.username)
            table.add_row("Département", user.department.name)
            console.print(table)
            click.echo(f"Token d'accès : {token}")
            click.echo("\nVeuillez conserver ce token pour les prochaines opérations.")
        else:
            # En cas d'échec, afficher le message d'erreur
            click.echo(f"Erreur lors de l'authentification : {result}")
    except Exception as e:
        log_error(
            logger,
            "Erreur lors de l'authentification",
            exception=e
        )
        # sentry_sdk.capture_exception(e)
        click.echo(f"Erreur : {e}")

@users.command(name='update-users')
@require_permission('can_manage_users')
def update(user_data):
    """
    Mettre à jour un utilisateur avec les données fournies.
    """
    user_id = click.prompt('ID de l\'utilisateur à mettre à jour', type=int)

    # Demander les informations de l'utilisateur
    updates = {}
    if click.confirm('Voulez-vous mettre à jour le nom d\'utilisateur ?'):
        updates['username'] = click.prompt('Nom d\'utilisateur')
    if click.confirm('Voulez-vous mettre lemots de passe ?'):
        updates['password'] = click.prompt('Mot de passe', hide_input=True, confirmation_prompt=True)
    if click.confirm('Voulez-vous mettre  le nom complet ?'):
        updates['fullname'] = click.prompt('Nouveau nom complet', default='')
    if click.confirm('Voulez-vous mettre à jour l\'adresse email ?'):
        updates['email'] = click.prompt('Nouvelle adresse email', default='')
    if click.confirm('Voulez-vous mettre    le numéro de téléphone ?'):
        updates['phone'] = click.prompt('Nouveau numéro de téléphone', default='')
    if click.confirm('Voulez-vous mettre le département ?'):
        session = SessionLocal()
        try:
            departments = session.query(Department).all()
            if not departments:
                click.echo("Aucun département disponible.")
                # session.close()
                return
            dept_choices = {str(dept.id): dept.name for dept in departments}
            click.echo('Départements disponibles :')
            for dept_id, dept_name in dept_choices.items():
                click.echo(f"{dept_id}. {dept_name}")
            department_id = click.prompt('Sélectionnez un département', type=click.Choice(dept_choices.keys()))
            updates['department_id'] = int(department_id)
        finally:
            session.close()
    # Vérifier si des mises à jour ont été demandées
    if not updates:
        click.echo("Aucune mise à jour demandée.")
        return
    
    # Mettre à jour l'utilisateur via le contrôleur
    try:
        controller = UserController()
        user = controller.update_user(user_id, updates)
        controller.close()

        if user:
            # Journaliser la mise à jour de l'utilisateur
            log_info(
                logger,
                f"Utilisateur mis à jour : {user.username}",
                user_id=user.id,
                department = user.department.name
            )
    
            click.echo(f"Utilisateur mis à jour avec succès : {user.username}")
            console = Console()
            table = Table(title="Utilisateur mis à jour avec succès", show_header=False)
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
            click.echo("Erreur lors de la mise à jour de l'utilisateur.")
    except Exception as e:
        # Capture des erreurs inattendues
        log_error(
            logger,
            "Erreur lors de la mise à jour de l'utilisateur",
            exception=e
        )
        click.echo(f"Erreur : {e}")
