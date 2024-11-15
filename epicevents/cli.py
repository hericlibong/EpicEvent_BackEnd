import click
from cli.users import users
from cli.clients import clients
from cli.contracts import contracts
from cli.events import events

@click.group()
def cli():
    """Interface en ligne de commande pour Epic Events."""
    pass

# Ajouter les groupes de commandes
cli.add_command(users)
cli.add_command(clients)
cli.add_command(contracts)
cli.add_command(events)

if __name__ == '__main__':
    cli()
