# cli/events.py
import click
from rich.console import Console
from rich.table import Table
from controllers.event_controller import EventController
from controllers.user_controller import UserController
from controllers.client_controller import ClientController
from controllers.contract_controller import ContractController
from utils.decorators import require_permission

@click.group()
def events():
    """Commandes pour gérer les événements."""
    pass

@events.command(name ='create-event')
@require_permission('can_create_events')
def create(user_data):
    """
    Créer un nouvel évènement
    """
    client_id = click.prompt('ID du client', type=int)

    # Vérifier que le client appartient à l'utilisateur
    client_controller = ClientController()
    client = client_controller.get_client_by_id(client_id)
    if client.sales_contact_id != user_data['user_id']:
        click.echo("Vous n'êtes pas responsable de ce client.")
        client_controller.close()
        return
    
    # Vérifier que le client a un contrat signé
    contract_controller = ContractController()
    contracts = contract_controller.get_contracts_by_client_id(client_id)
    signed_contracts = [c for c in contracts if c.status]
    if not signed_contracts:
        click.echo("Le client n'a pas de contrat signé.")
        contract_controller.close()
        client_controller.close()
        return
    
    # Collecte des informations de l'événement
    event_date_start = click.prompt('Date de début de l\'évènement (JJ/MM/AAAA HH:MM)', type=str)
    event_date_end = click.prompt('Date de fin de l\'évènement (JJ/MM/AAAA HH:MM)', type=str)
    location = click.prompt('Lieu de l\'évènement', default='')
    attendees = click.prompt('Nombre de participants', type=int, default=0)
    notes = click.prompt('Notes supplémentaires', default='')

    event_data = {
        'contract_id': signed_contracts[0].id,  # Utiliser le premier contrat signé
        'event_date_start': event_date_start,
        'event_date_end': event_date_end,
        'location': location,
        'attendees': attendees,
        'notes': notes
    }

    event_controller = EventController()
    event = event_controller.create_event(event_data)
    event_controller.close()
    contract_controller.close()
    client_controller.close()

    if event:

        console = Console()
        table = Table(title="Evènement créé avec succès", show_header=False)

        table.add_column("champ", style="bold cyan")
        table.add_column("valeur", style="bold magenta")

        table.add_row("ID", str(event.id))
        table.add_row("Numéro de contrat", str(event.contract_id))
        table.add_row("Date de début", event.event_date_start.strftime("%d/%m/%Y %H:%M"))
        table.add_row("Date de fin", event.event_date_end.strftime("%d/%m/%Y %H:%M"))
        table.add_row("Lieu", event.location)
        table.add_row("Nombre de participants", str(event.attendees))
        table.add_row("Notes", event.notes)
        console.print(table)
        
    else:
        click.echo("Erreur lors de la création de l'évènement.")


@events.command(name='update-own')
@require_permission('can_modify_own_events')
def update(user_data):
    """
    Mettre à jour un évènement dont vous êtes responsable.
    """

    event_id = click.prompt('ID de l\'évènement à mettre à jour', type=int)

    event_controller = EventController()
    event = event_controller.get_event_by_id(event_id)
    
    # Vérifier que l'évènement appartient à l'utilisateur
    if event.support_contact_id != user_data['user_id']:
        click.echo("Vous n'êtes pas responsable de cet évènement. Vous ne pouvez pas le modifier.")
        event_controller.close()
        return
    
    # Collecte les nouvelles informations de l'évènement pour la mise à jour
    event_date_start = click.prompt('Nouvelle date de début de l\'évènement (JJ/MM/AAAA HH:MM)', type=str)
    event_date_end = click.prompt('Nouvelle date de fin de l\'évènement (JJ/MM/AAAA HH:MM)', type=str)
    location = click.prompt('Nouveau lieu de l\'évènement', default=event.location)
    attendees = click.prompt('Nouveau nombre de participants', type=int, default=event.attendees)   
    notes = click.prompt('Nouvelles notes supplémentaires', default=event.notes)

    event_data = {
        'event_date_start': event_date_start,
        'event_date_end': event_date_end,
        'location': location,
        'attendees': attendees,
        'notes': notes
    }

    updated_event = event_controller.update_event(event_id, event_data)
    event_controller.close()

    if updated_event:
        click.echo(f"Evènement mis à jour avec succès : ID {updated_event.id}")
    else:
        click.echo("Erreur lors de la mise à jour de l'évènement.")

    

@events.command()
@require_permission('can_assign_support')
def assign_support(user_data): # Pourquoi user_data en argument alors qu'il n'est pas appelé?
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




# Commandes pour filtrer les évènements pour le support et la gestion
@events.command(name='list-filtered')
@require_permission('can_filter_events')
@click.option('--no-support', is_flag=True, help='Afficher uniquement les événements sans contact support') 
def list_filtered_events(user_data, no_support):
    """
    Afficher la liste des événements filtrés par le support.
    """
    event_controller = EventController()
    department = user_data.get('department')

    if department == 'Support':
        # Afficher les évènements assignés à ce support
        events = event_controller.get_events_by_support(user_data['user_id'])
    elif department == 'Gestion':
        # Afficher tous les évènements
        events = event_controller.get_all_events()
        # Filtrer les évènements sans contact support si l'option --no-support est activée
        if no_support:
            events = [event for event in events if event.support_contact_id is None]
    else:
        # Pour les autres départments, afficher le refus d'accès
        click.echo("Accès refusé. Vous n'êtes pas autorisé à accéder à cette commande.")
        event_controller.close()
        return
    
    event_controller.close()  # Pourquoi fermer une seconde fois?

    if not events:
        click.echo("Aucun événement trouvé.")
        return
    
    # Afficher les évènements avec Rich
    console = Console()
    table = Table(
        title="[bold cyan]Liste des Evènements[/]",
        show_header=True,
        show_lines=True,
        header_style="bold magenta")
    table.add_column("ID", style="dim")
    table.add_column("Numéro de contrat")
    table.add_column("Nom du client")
    table.add_column("Contact client", width=25)
    table.add_column("Date de début")
    table.add_column("Date de fin")
    table.add_column("Contact support")
    table.add_column("Lieu")
    table.add_column("Nombre de participants")
    table.add_column("Notes")
    table.add_column("Date de création", style="dim")
    table.add_column("Date de modification", style="dim")

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
            event.notes or "N/A",
            event.date_created.strftime("%d/%m/%Y %H:%M"),
            event.date_updated.strftime("%d/%m/%Y %H:%M")
        )
    console.print(table)

@events.command(name='list-all')
def list_all_events():
    """
    Afficher la liste des événements en lecture seule.
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
    event_controller.close()

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
    table.add_column("Contact client", width=25)
    table.add_column("Date de début")
    table.add_column("Date de fin")
    table.add_column("Contact support")
    table.add_column("Lieu")
    table.add_column("Nombre de participants")
    table.add_column("Notes")
    table.add_column("Date de création", style="dim")
    table.add_column("Date de modification", style="dim")

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
            event.notes or "N/A",
            event.date_created.strftime("%d/%m/%Y %H:%M"),
            event.date_updated.strftime("%d/%m/%Y %H:%M")
        )
    console.print(table)
        
