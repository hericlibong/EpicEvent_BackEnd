import click
from rich.console import Console
from rich.table import Table
from controllers.user_controller import UserController
from controllers.client_controller import ClientController
from controllers.contract_controller import ContractController
from controllers.event_controller import EventController

from models import Department  # Adjust the import path as necessary
from config import SessionLocal


@click.group()
def cli():
    pass

@cli.command()
def list_events():
    """
    Afficher la liste des événements.
    """
    controller = UserController()
    token = click.prompt('Veuillez entrer votre Token d\'accès')

    # Vérifier l'authentification
    user_data = controller.verify_token(token)
    if not user_data:
        click.echo("Token invalide ou expiré. Authentification échouée.")
        return
    event_controller = EventController()
    events = event_controller.get_all_events()

    if not events:
        click.echo("Aucun événement trouvé.")
        return
    
    console = Console()
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim")
    table.add_column("Numéro de contrat")
    table.add_column("Nom du client")
    table.add_column("Contact client")
    table.add_column("Date de début")
    table.add_column("Date de fin")
    table.add_column("Contact support")
    table.add_column("Lieu")
    table.add_column("Nombre de participants")
    table.add_column("Notes")

    for event in events:
        table.add_row(
            str(event.id),
            str(event.contract_id),
            event.contract.client.fullname if event.contract and event.contract.client else "Non défini",
            (f"{event.contract.client.email or 'N/A'} / {event.contract.client.phone or 'N/A'}"
            if event.contract and event.contract.client else "Non défini"),
            event.event_date_start.strftime("%d/%m/%Y %H:%M") if event.event_date_start else "N/A",
            event.event_date_end.strftime("%d/%m/%Y %H:%M") if event.event_date_end else "N/A",
            event.support_contact.fullname if event.support_contact else "Non défini",
            event.location or "N/A",
            str(event.attendees) if event.attendees is not None else "0",
            event.notes or "N/A"
        )
    console.print(table)


@cli.command()
def list_contracts():
    """
    Afficher la liste des contrats.
    """
    controller = UserController()
    token = click.prompt('Veuillez entrer votre Token d\'accès')

    # Vérifier l'authentification
    user_data = controller.verify_token(token)
    if not user_data:
        click.echo("Token invalide ou expiré. Authentification échouée.")
        return
    contract_controller = ContractController()
    contracts = contract_controller.get_all_contracts()

    if not contracts:
        click.echo("Aucun contrat trouvé.")
        return
    
    console = Console()
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim")
    table.add_column("Nom du client")
    table.add_column("Commercial concerné")
    table.add_column("Motant total")
    table.add_column("Montant restant")
    table.add_column("Date de création")
    table.add_column("Statut")

    for contract in contracts:
        table.add_row(
            str(contract.id), 
            contract.client.fullname,
            contract.sales_contact.fullname,
            str(contract.amount),
            str(contract.remaining_amount),
            contract.date_created.strftime("%d/%m/%Y %H:%M"),
            "Signé" if contract.status else "En attente"
            )
    console.print(table)    

@cli.command()
def list_clients():
    """
    Afficher la liste des clients.
    """
    controller = UserController()
    token = click.prompt('Veuillez entrer votre Token d\'accès')

    # Vérifier k'authentification
    user_data = controller.verify_token(token)
    if not user_data:
        click.echo("Token invalide ou expriré. Authentification échouée.")
        return
    client_controller = ClientController()
    clients = client_controller.get_all_clients()

    if not clients:
        click.echo("Aucun client trouvé.")
        return
    
    console = Console()
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim")
    table.add_column("Nom")
    table.add_column("Email")
    table.add_column("Téléphone")

    for client in clients:
        table.add_row(
            str(client.id), 
            client.fullname,
            client.email or "",
            client.phone or "", 
            )
    console.print(table)

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
        print("Copiez et collez le token pour accéder aux autres commandes.")
    else:
        print("Authentification échouée.")

if __name__ == '__main__':
    cli()
