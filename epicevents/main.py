import click
import sentry_sdk
import os
import logging
from sentry_sdk.integrations.logging import LoggingIntegration
from utils.logger import log_info, log_error, get_logger
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Initialiser Sentry avec le DSN depuis la variable d'environnement
sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    integrations=[
        LoggingIntegration(
            level=logging.INFO,
            event_level=logging.ERROR
        )
    ],
    traces_sample_rate=1.0,  # Capture 100% des traces (peut être ajusté)
    environment=os.getenv("ENVIRONMENT", "development")  # Environnement de déploiement
)

# Obtenir un logger spécifique pour ce module
logger = get_logger('cli')

from cli.users import users
from cli.clients import clients
from cli.contracts import contracts
from cli.events import events


@click.group()
def cli():
    """Interface en ligne de commande pour Epic Events."""
    pass


@cli.result_callback()
def process_result(result, **kwargs):
    """Capture globale des exceptions inattendues."""
    try:
        # Vérifier si une exception réelle est remontée
        if isinstance(result, Exception):
            raise result
    except Exception as e:
        log_error(logger, "Une erreur inattendue a été capturée.", exception=e)
        click.echo("Une erreur inattendue a été capturée.")


@cli.command()
def sample_command():
    """Commande d'exemple avec journalisation."""
    log_info(logger, "Exécution de sample_command")
    try:
        # Simuler une opération
        result = 10 / 2
        log_info(logger, f"Résultat de la division : {result}")
    except Exception as e:
        log_error(logger, "Erreur lors de l'exécution de sample_command", exception=e)
        raise


# Ajouter les groupes de commandes
cli.add_command(users)
cli.add_command(clients)
cli.add_command(contracts)
cli.add_command(events)


if __name__ == '__main__':
    cli()
