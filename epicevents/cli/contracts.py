# cli/contracts.py
import click
from rich.console import Console
from rich.table import Table
from controllers.contract_controller import ContractController
from controllers.user_controller import UserController
from controllers.client_controller import ClientController
from utils.decorators import require_permission
from click_aliases import ClickAliasedGroup


@click.group(cls=ClickAliasedGroup)
def contracts():
    """Commandes pour gérer les contrats."""
    pass

@contracts.command()
@require_permission('can_create_contracts')
def create(user_data):
    """
    Créer un nouveau contrat
    """

    # Collecte des informations du contrat
    client_id = click.prompt('ID du client', type=int)
    amount = click.prompt('Montant total', type=float)
    remaining_amount = click.prompt('Montant restant', type=float)
    status = click.prompt('Statut (1 pour signé, 0 pour en attente)', type=int)
    sales_contact_id = click.prompt('ID du commercial', type=int)

    contract_data = {
        'client_id': client_id,
        'amount': amount,
        'remaining_amount': remaining_amount,
        'status': bool(status),
        'sales_contact_id': sales_contact_id
    }

    # Créer le contrat via le contrôleur
    contract_controller = ContractController()
    contract = contract_controller.create_contract(contract_data)
    contract_controller.close()

    if contract:
        click.echo(f"Contrat créé avec succès : ID {contract.id}")
    else:
        click.echo("Erreur lors de la création du contrat.")


@contracts.command(name='update-all')
@require_permission('can_modify_all_contracts')
def update_any_contract(user_data):
    """
    Mettre à jour un contrat existant.
    """
    contract_id = click.prompt('ID du contrat à mettre à jour', type=int)

    # Collecte des informations du contrat
    amount = click.prompt('Montant total', type=float)
    remaining_amount = click.prompt('Montant restant', type=float)
    status = click.prompt('Statut (1 pour signé, 0 pour en attente)', type=int)

    contract_data = {
        'amount': amount,
        'remaining_amount': remaining_amount,
        'status': bool(status),
        'sales_contact_id': user_data.get('id')
    }

    # Mettre à jour le contrat via le contrôleur
    contract_controller = ContractController()
    contract = contract_controller.update_contract(contract_id, contract_data)
    contract_controller.close()

    if contract:
        click.echo(f"Contrat mis à jour avec succès : ID {contract.id}")
    else:
        click.echo("Erreur lors de la mise à jour du contrat.")

# Commande pour mettre à jour un contrat pour les commerciaux
@contracts.command(name='update-own')
@require_permission('can_modify_own_contracts')
def update_own_contract(user_data):
    """
    Mettre à jour un contrat dont vous êtes responsable.
    """
    contract_id = click.prompt('ID du contrat à mettre à jour', type=int)

    # Vérifier que le contrat appartient à l'utilisateur
    contract_controller = ContractController()
    contract = contract_controller.get_contract_by_id(contract_id)
    if not contract:
        click.echo("Contrat introuvable.")
        contract_controller.close()
        return
    
    client_controller = ClientController()
    client = client_controller.get_client_by_id(contract.client_id)
    if not client:
        click.echo("Client associé au contrat non trouvé.")
        contract_controller.close()
        client_controller.close()
        return

    if client.sales_contact_id != user_data['user_id']:
        click.echo("Vous n'êtes pas responsable de ce client.")
        contract_controller.close()
        client_controller.close()
        return
    
    # Collecte des informations du contrat
    amount = click.prompt('Nouveau montant total', default=contract.amount, type=float)
    remaining_amount = click.prompt('Nouveau montant restant', default=contract.remaining_amount, type=float)
    status = click.prompt('Nouveau statut (1 pour signé, 0 pour en attente)', default=int(contract.status), type=int)

    contract_data = {
        'amount': amount,
        'remaining_amount': remaining_amount,
        'status': bool(status),
    }

    # Mettre à jour le contrat via le contrôleur
    updated_contract = contract_controller.update_contract(contract_id, contract_data)
    contract_controller.close()
    client_controller.close()

    if updated_contract:
        click.echo(f"Contrat mis à jour avec succès : ID {updated_contract.id}")
    else:
        click.echo("Erreur lors de la mise à jour du contrat.")


# Commandes pour filtrer les contrats pour les commerciaux et la gestion
@contracts.command(name='list-filtered', aliases=[''])
@require_permission('can_filter_contracts')
@click.option('--status', type=click.Choice(['signed', 'unsigned']), help='Filtrer par statut du contrat ("signed" ou "unsigned")')
@click.option('--payment', type=click.Choice(['paid', 'unpaid']), help='Filtrer par paiement("paid" ou "unpaid")')
def list_contract_filtered(user_data, status, payment):
    """
    Afficher la liste des contrats avec options de filtrage.
    """
    contract_controller = ContractController()
    department = user_data.get('department')

    if department == 'Gestion':
        contracts = contract_controller.get_all_contracts()
    elif department == 'Commercial':
        contracts = contract_controller.get_contract_by_sales_contact(user_data['user_id'])
    else:
        # Pour les autres départements, récupérez les contrats en lecture seule si nécessaire
        contracts = contract_controller.get_all_contracts()

    # Appliquer les filtres
    if status == 'signed':
        contracts = [c for c in contracts if c.status]
    elif status == 'unsigned':
        contracts = [c for c in contracts if not c.status]

    if payment == 'paid':
        contracts = [c for c in contracts if c.remaining_amount == 0]
    elif payment == 'unpaid':
        contracts = [c for c in contracts if c.remaining_amount > 0]

    contract_controller.close()

    # if not contracts:
    #     if status and not payment:
    #         if status == 'signed':
    #             click.echo("Aucun contrat signé trouvé.")
    #         else:
    #             click.echo("Aucun contrat non signé trouvé.")
    #     elif payment and not status:
    #         if payment == 'paid':
    #             click.echo("Aucun contrat payé trouvé.")
    #         else:
    #             click.echo("Aucun contrat impayé trouvé.")
    #     elif status or payment:
    #         click.echo(f"Aucun contrat trouvé avec statut '{status}' et paiement '{payment}'.")
    #     else:
    #         click.echo("Aucun contrat trouvé.")
    #     return

    if not contracts:
        # Construire le message d'erreur personnalisé
        criteria = []
        if status:
            criteria.append(f"statut '{status}'")
        if payment:
            criteria.append(f"paiement '{payment}'")
        if criteria:
            criteria_str = " et ".join(criteria)
            click.echo(f"Aucun contrat trouvé avec les critères : {criteria_str}.")
        else:
            click.echo("Aucun contrat trouvé.")
        return



    console = Console()
    table = Table(
        title="Liste des contrats",
        show_header=True, header_style="bold magenta",
        show_lines=True)
    table.add_column("ID", style="dim")
    table.add_column("Nom du client")
    table.add_column("Commercial")
    table.add_column("Montant total")
    table.add_column("Montant restant")
    table.add_column("Date de création")
    table.add_column("Statut")

    for contract in contracts:
        table.add_row(
            str(contract.id),
            contract.client.fullname if contract.client else "N/A",
            contract.sales_contact.fullname if contract.sales_contact else "N/A",
            str(contract.amount),
            str(contract.remaining_amount),
            contract.date_created.strftime("%d/%m/%Y %H:%M"),
            "Signé" if contract.status else "En attente"
        )
    console.print(table)

    

@contracts.command(name='list-all')
def list_all_contracts():
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