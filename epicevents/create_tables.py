from config import engine
from models.base import Base
from models.client import Client
from models.contract import Contract
from models.event import Event
from models.user import User

def create_tables():
    Base.metadata.create_all(bind=engine)
    print("Les tables ont été créées avec succès")

if __name__ == '__main__':
    create_tables()