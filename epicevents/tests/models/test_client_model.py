import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base
from models.client import Client
from models.user import User
from models.department import Department

@pytest.fixture(scope='module')
def test_engine():
    # Utiliser SQLite en mémoire pour des tests isolés
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    return engine

@pytest.fixture(scope='function')
def session(test_engine):
    # Crée une session pour chaque test
    connection = test_engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    session = Session()

    yield session  # Donne la session au test

    # Nettoie après le test
    session.close()
    transaction.rollback()
    connection.close()

def test_create_client(session):
    # Créer un département
    department = Department(name='Commercial', description='Service commercial')
    session.add(department)
    session.commit()

    # Crée un utilisateur (sales contact)
    sales_contact = User(username='salesuser',
                         hashed_password='hashedpassword',
                         fullname='Sales User',
                         email='salesuser@email.com',
                         phone='1234567890',
                         department=department)
    session.add(sales_contact)
    session.commit()

    # Crée un client
    client = Client(fullname='Test Client',
                    email='testclient@email.com',
                    phone='0987654321',
                    company_name='Test Company',
                    sales_contact=sales_contact)
    session.add(client)
    session.commit()

    # Vérifie que le client est créé correctement
    created_client = session.query(Client).filter_by(email='testclient@email.com').one()
    assert created_client.fullname == 'Test Client'
    assert created_client.company_name == 'Test Company'
    assert created_client.sales_contact.username == 'salesuser'

def test_update_client(session):
    # Crée un client
    client = Client(fullname='Old Name',
                    email='oldemail@email.com',
                    phone='1234567890',
                    company_name='Old Company')
    session.add(client)
    session.commit()

    # Modifie le client
    client.fullname = 'New Name'
    client.company_name = 'New Company'
    session.commit()

    # Vérifie les mises à jour
    updated_client = session.query(Client).filter_by(email='oldemail@email.com').one()
    assert updated_client.fullname == 'New Name'
    assert updated_client.company_name == 'New Company'

def test_cascade_delete_client_contracts(session):
    # Crée un département
    from models.department import Department
    department = Department(name='Commercial', description='Service commercial')
    session.add(department)
    session.commit()

    # Crée un utilisateur (sales contact)
    from models.user import User
    sales_contact = User(username='salesuser',
                         hashed_password='hashedpassword',
                         fullname='Sales User',
                         email='salesuser@email.com',
                         phone='1234567890',
                         department=department)
    session.add(sales_contact)
    session.commit()

    # Crée un client
    from models.client import Client
    client = Client(fullname='Test Client',
                    email='testclient@email.com',
                    phone='0987654321',
                    company_name='Test Company',
                    sales_contact=sales_contact)
    session.add(client)
    session.commit()

    # Crée un contrat pour ce client
    from models.contract import Contract
    contract = Contract(client=client,
                        sales_contact=sales_contact,
                        status=True,
                        amount=5000.0,
                        remaining_amount=2500.0)
    session.add(contract)
    session.commit()

    # Vérifie que le contrat a été créé
    created_contract = session.query(Contract).filter_by(client_id=client.id).first()
    assert created_contract is not None

    # Supprime le client
    session.delete(client)
    session.commit()

    # Vérifie que le contrat associé est supprimé
    deleted_contract = session.query(Contract).filter_by(client_id=client.id).first()
    assert deleted_contract is None






