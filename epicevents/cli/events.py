# cli/events.py
import click
from rich.console import Console
from rich.table import Table
from controllers.event_controller import EventController
from controllers.user_controller import UserController
from utils.decorators import require_permission

@click.group()
def events():
    """Commandes pour gérer les événements."""
    pass

@events.command()
@require_permission('can_modify_all_events')
def assign_support(): # Pourquoi user_data en argument alors qu'il n'est pas appelé?
    """
    Assigner un contact support à un événement.
    """
    event_id = click.prompt('ID de l\'événement à mettre à jour', type=int)
    support_user_id = click.prompt('ID du contact support', type=int)

    event_controller = EventController()
    success = event_controller.assign_support(event_id, support_user_id)
    event_controller.close()
    
    if success:
        click.echo(f"Contact support assigné avec succès à l'événement ID {event_id}")
    else:
        click.echo("Erreur lors de l'assignation du contact support.")


@events.command()
def list():
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
    table = Table(
        title="[bold cyan]Tableau des Evènements[/]",
        show_header=True, 
        show_lines=True,
        header_style="bold magenta")
    table.add_column("ID", style="dim")
    table.add_column("Numéro de contrat")
    table.add_column("Nom du client")
    table.add_column("Contact client", width=30)
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
            (f"Email:{event.contract.client.email or 'N/A'} | tel:{event.contract.client.phone or 'N/A'}"
            if event.contract and event.contract.client else "Non défini"),
            event.event_date_start.strftime("%d/%m/%Y %H:%M") if event.event_date_start else "N/A",
            event.event_date_end.strftime("%d/%m/%Y %H:%M") if event.event_date_end else "N/A",
            event.support_contact.fullname if event.support_contact else "Non défini",
            event.location or "N/A",
            str(event.attendees) if event.attendees is not None else "0",
            event.notes or "N/A"
        )
    console.print(table)