import click
import sentry_sdk

# Initialiser Sentry
sentry_sdk.init(
    dsn="https://7f8ea82782f16c67853ab71054b6a3cd@o4508367841263616.ingest.de.sentry.io/4508367972794448",
    traces_sample_rate=1.0  # Capture 100% des traces (peut être ajusté)
)

from cli.users import users
from cli.clients import clients
from cli.contracts import contracts
from cli.events import events

@click.group()
def cli():
    """Interface en ligne de commande pour Epic Events."""
    pass

@cli.resultcallback()
def process_result(result, **kwargs):
    """Capture globale des exceptions inattendues."""
    try:
        if result is None:
            raise RuntimeError("Erreur inattendue globale.")
    except Exception as e:
        sentry_sdk.capture_exception(e)
        click.echo("Une erreur inattendue a été capturée.")

# Ajouter les groupes de commandes
cli.add_command(users)
cli.add_command(clients)
cli.add_command(contracts)
cli.add_command(events)



if __name__ == '__main__':
    cli()
