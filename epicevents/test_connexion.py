from config import engine
from sqlalchemy import text
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_database_connection(retries=3, delay=2):
    for attempt in range(retries):
        try:
            with engine.connect() as connection:
                result = connection.execute(text('SELECT 1'))
                logger.info("Connexion à la base de données réussie")
                return True
        except Exception as e:
           logger.warning(f"Echec de la connexion à la base de données : {e}. Tentative {attempt + 1} de {retries}")
        time.sleep(delay)
    logger.error("Impossible de se connecter à la base de données")
    return False

# Appel de la fonctionn pour tester
test_database_connection()