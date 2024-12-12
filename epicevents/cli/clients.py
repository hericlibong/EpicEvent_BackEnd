# cli/clients.py
import click
from rich.console import Console
from rich.table import Table
from controllers.client_controller import ClientController
from controllers.user_controller import UserController
from utils.decorators import require_permission
from utils.logger import log_info, log_error, get_logger


logger = get_logger('clients')


@click.group()
def clients():
    """Commandes pour gérer les clients."""
    pass


@clients.command()
@require_permission('can_create_clients')
def create(user_data):
    """
    Créer un nouveau client.
    """
    # Collecte des informations du client
    fullname = click.prompt('Nom complet')
    email = click.prompt('Adresse email', default='')
    phone = click.prompt('Numéro de téléphone', default='')
    company_name = click.prompt('Nom de l\'entreprise', default='')

    client_data = {
        'fullname': fullname,
        'email': email,
        'phone': phone,
        'company_name': company_name,
        'sales_contact_id': user_data.get('user_id')  # Identifiant du commercial
    }

    # Créer le client via le contrôleur
    client_controller = ClientController()
    try:
        client = client_controller.create_client(client_data)  # Appel au contrôleur

        if client:
            log_info(
                logger,
                f"Client créé avec succès : {client.fullname} (ID : {client.id}),\n"
                f" Commercial : {client.sales_contact.fullname}"
                )

            # Afficher les informations du client créé
            console = Console()
            table = Table(title="Client créé avec succès", show_header=False)
            table.add_column("Champ", style="bold cyan")
            table.add_column("Valeur", style="bold magenta")
            table.add_row("ID", str(client.id))
            table.add_row("Nom complet", client.fullname)
            table.add_row("Email", client.email)
            table.add_row("Téléphone", client.phone)
            table.add_row("Entreprise", client.company_name)
            table.add_row("Commercial", client.sales_contact.fullname)
            console.print(table)
        else:
            click.echo("Erreur lors de la création du client.")

    except ValueError as e:
        # Message utilisateur pour une erreur contrôlée
        click.echo(f"Erreur lors de la création du client : {e}")
    except Exception as e:
        # Erreur inattendue
        log_error(
                logger,
                "Erreur lors de la création de l'utilisateur",
                exception=e
            )
        # Message d'erreur inattendue dans Sentry
        click.echo("Une erreur inattendue est survenue lors de la création du client.")
    finally:
        client_controller.close()  # Nettoyer les ressources


@clients.command(name='update')
@require_permission('can_modify_all_clients')
def update_any_client(user_data):
    """
    Mettre à jour les clients  (réservé aux Gestionnaires).
    """
    client_id = click.prompt('ID du client à mettre à jour', type=int)
    client_controller = ClientController()

    try:
        client = client_controller.get_client_by_id(client_id)
        if not client:
            raise ValueError("Client non trouvé.")

        # Collecte des informations du client
        fullname = click.prompt('Nouveau nom complet', default=client.fullname)
        email = click.prompt('Nouvelle adresse email', default=client.email)
        phone = click.prompt('Nouveau numéro de téléphone', default=client.phone)
        company_name = click.prompt('Nouveau nom de l\'entreprise', default=client.company_name)
        sales_contact_id = click.prompt('Nouveau commercial', default=client.sales_contact_id)

        client_data = {
            'fullname': fullname,
            'email': email,
            'phone': phone,
            'company_name': company_name,
            'sales_contact_id': sales_contact_id
        }

        # Mettre à jour le client via le contrôleur
        updated_client = client_controller.update_client(client_id, client_data)

        if updated_client:
            log_info(
                logger,
                f"Client mis à jour avec succès : {updated_client.fullname} (ID : {updated_client.id})"
            )
            click.echo(f"Client mis à jour avec succès : {updated_client.fullname}")
            console = Console()
            table = Table(title="Client mis à jour avec succès", show_header=False)
            table.add_column("Champ", style="bold cyan")
            table.add_column("Valeur", style="bold magenta")
            table.add_row("ID", str(updated_client.id))
            table.add_row("Nom complet", updated_client.fullname)
            table.add_row("Email", updated_client.email)
            table.add_row("Téléphone", updated_client.phone)
            table.add_row("Entreprise", updated_client.company_name)
            console.print(table)
        else:
            click.echo("Erreur lors de la mise à jour du client.")

    except ValueError as e:
        click.echo(f"Erreur lors de la mise à jour du client : {e}")
    except Exception as e:
        log_error(
                logger,
                "Erreur lors de la mise à jour du client",
                exception=e
            )
        click.echo("Une erreur inattendue est survenue lors de la mise à jour du client.")
    finally:
        client_controller.close()


@clients.command(name='update-own')
@require_permission('can_modify_own_clients')
def update_own_client(user_data):
    """
    Mettre à jour un client dont vous êtes responsable (Commerciaux).
    """
    client_id = click.prompt('ID du client à mettre à jour', type=int)

    # Vérifier que le client appartient à l'utilisateur
    client_controller = ClientController()

    try:
        client = client_controller.get_client_by_id(client_id)
        if not client:
            click.echo("Client non trouvé.")
            client_controller.close()
            return

        if client.sales_contact_id != user_data['user_id']:
            click.echo("Vous n'êtes pas responsable de ce client.")
            client_controller.close()
            return

        # Collecte des informations du client
        fullname = click.prompt('Nouveau nom complet', default=client.fullname)
        email = click.prompt('Nouvelle adresse email', default=client.email)
        phone = click.prompt('Nouveau numéro de téléphone', default=client.phone)

        client_data = {
            'fullname': fullname,
            'email': email,
            'phone': phone,
        }

        # Mettre à jour le client via le contrôleur
        updated_client = client_controller.update_client(client_id, client_data)
        client_controller.close()

        if updated_client:
            log_info(
                logger,
                f"Client mis à jour avec succès : {updated_client.fullname} (ID : {updated_client.id}),\n"
                f" Commercial : {user_data['username']})"
            )
            click.echo(f"Données client : {updated_client.fullname}")
            console = Console()
            table = Table(title="Client mis à jour avec succès", show_header=False)
            table.add_column("Champ", style="bold cyan")
            table.add_column("Valeur", style="bold magenta")
            table.add_row("ID", str(updated_client.id))
            table.add_row("Nom complet", updated_client.fullname)
            table.add_row("Email", updated_client.email)
            table.add_row("Téléphone", updated_client.phone)
            table.add_row("Entreprise", updated_client.company_name)
            console.print(table)
        else:
            click.echo("Erreur lors de la mise à jour du client.")

    except ValueError as e:
        click.echo(f"Erreur lors de la mise à jour du client : {e}")
    except Exception as e:
        log_error(
                logger,
                "Erreur lors de la mise à jour du client",
                exception=e
            )
        click.echo("Une erreur inattendue est survenue lors de la mise à jour du client.")
    finally:
        client_controller.close()


@clients.command(name='delete-own')
@require_permission('can_modify_own_clients')
def delete_own_client(user_data):
    """
    Supprimer un client dont vous êtes responsable.
    """
    client_id = click.prompt('ID du client à supprimer', type=int)
    client_controller = ClientController()

    try:
        client = client_controller.get_client_by_id(client_id)
        if not client:
            raise ValueError("Client non trouvé.")

        if client.sales_contact_id != user_data['user_id']:
            raise ValueError("Vous n'êtes pas responsable de ce client.")

        success = client_controller.delete_client(client_id)
        if success:
            log_info(
                logger,
                f"Client supprimé (own) : ID {client_id}, Commercial : {user_data['username']}"
            )
            click.echo(f"Client supprimé avec succès : ID {client_id}")
        else:
            click.echo("Erreur lors de la suppression du client.")

    except ValueError as e:
        click.echo(f"Erreur lors de la suppression du client : {e}")
    except Exception as e:
        log_error(
            logger,
            "Erreur lors de la suppression du client (own)",
            exception=e
        )
        click.echo("Une erreur inattendue est survenue lors de la suppression du client.")
    finally:
        client_controller.close()


@clients.command(name='delete-all')
@require_permission('can_modify_all_clients')
def delete_any_client():
    """
    Supprimer un client quelconque.
    """
    client_id = click.prompt('ID du client à supprimer', type=int)
    client_controller = ClientController()

    try:
        success = client_controller.delete_client(client_id)
        if success:
            log_info(
                logger,
                f"Client supprimé (all) : ID {client_id}"
            )
            click.echo(f"Client supprimé avec succès : ID {client_id}")
        else:
            click.echo("Erreur lors de la suppression du client.")

    except ValueError as e:
        click.echo(f"Erreur lors de la suppression du client : {e}")
    except Exception as e:
        log_error(
            logger,
            "Erreur lors de la suppression du client (all)",
            exception=e
        )
        click.echo("Une erreur inattendue est survenue lors de la suppression du client.")
    finally:
        client_controller.close()


@clients.command()
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
    table = Table(

        title="[bold cyan]Tableau des clients[/]",
        show_header=True,
        show_lines=True,
        header_style="bold magenta")
    table.add_column("ID", style="dim")
    table.add_column("Nom")
    table.add_column("Email")
    table.add_column("Téléphone")
    table.add_column("Entreprise")
    table.add_column("Date de création", style="dim")
    table.add_column("Dernière mise à jour", style="dim")
    table.add_column("Commercial")

    for client in clients:
        table.add_row(
            str(client.id),
            client.fullname,
            client.email or "",
            client.phone or "",
            client.company_name or "",
            client.date_created.strftime("%d/%m/%Y %H:%M:%S"),
            client.date_updated.strftime("%d/%m/%Y %H:%M:%S"),
            client.sales_contact.fullname

        )
    console.print(table)
