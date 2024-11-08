from config import engine
from sqlalchemy import text

try:
    with engine.connect() as connection:
        result = connection.execute(text('SELECT 1'))
        print("Connexion à la base de données réussie")
except Exception as e:
        print(f"Echec de la connexion à la base de données: {e}")