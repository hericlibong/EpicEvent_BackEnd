# cli/clients.py
import click
from rich.console import Console
from rich.table import Table
from controllers.client_controller import ClientController
from controllers.user_controller import UserController

@click.group()
def clients():
    """Commandes pour gérer les clients."""
    pass

@clients.command()
def list():
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