# cli/contracts.py
import click
from rich.console import Console
from rich.table import Table
from controllers.contract_controller import ContractController
from controllers.user_controller import UserController

@click.group()
def contracts():
    """Commandes pour gérer les contrats."""
    pass

@contracts.command()
def list():
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