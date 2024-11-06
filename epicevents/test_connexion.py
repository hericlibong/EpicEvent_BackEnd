from config import engine

try:
    with engine.connect() as connection:
        # result = connection.execute('SELECT 1')
        print("Connexion à la base de données réussie")
except Exception as e:
        print(f"Echec de la connexion à la base de données: {e}")