# tests/models/test_contract_model.py
import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from models.base import Base
from models.user import User
from models.client import Client
from models.contract import Contract
from models.department import Department
from models.event import Event
from sqlalchemy.exc import IntegrityError
from datetime import datetime


@pytest.fixture(scope='module')
def test_engine():
    # Crée une base de données SQLite en mémoire
    engine = create_engine('sqlite:///:memory:')

    # Activer les contraintes de clé étrangère sur chaque nouvelle connexion
    @event.listens_for(engine, 'connect')
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute('PRAGMA foreign_keys=ON')
        cursor.close()

    Base.metadata.create_all(engine)
    return engine

@pytest.fixture(scope='function')
def session(test_engine):
    # Crée une nouvelle session pour chaque test
    connection = test_engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    session = Session()

    yield session  # Exécute le test

    # Nettoyage après le test
    session.close()
    # transaction.rollback()
    connection.close()

@pytest.fixture(scope='function')
def department(session):
    dept = Department(name='Commercial', description='Commercial department')
    session.add(dept)
    session.commit()
    return dept

@pytest.fixture(scope='function')
def sales_contact(session, department):
    user = User(
        username='salesrep',
                hashed_password='hashedpassword',
                fullname='Sales Represenative',
                email = 'salesrep@example.com',
                phone = '1234567890',
                department = department
    )
    session.add(user)
    session.commit()
    return user

@pytest.fixture(scope='function')
def client(session, sales_contact):
    client = Client(
        fullname='John Doe',
        email='johndoe@example.com',
        phone='0987654321',
        company_name='Doe Enterprises',
        sales_contact=sales_contact
    )
    session.add(client)
    session.commit()
    return client

# Test 1 : Création d'un contrat
def test_create_contract(session, client, sales_contact):
    # Créer un contrat associé au client et au commercial
    contract = Contract(
        client=client,
        sales_contact=sales_contact,
        amount=10000.0,
        remaining_amount=5000.0,
        status=False
    )
    session.add(contract)
    session.commit()

    # Vérifier que le contrat a été créé
    retrieved_contract = session.query(Contract).filter_by(id=contract.id).one()
    assert retrieved_contract.client.fullname == 'John Doe'
    assert retrieved_contract.sales_contact.username == 'salesrep'
    assert retrieved_contract.amount == 10000.0
    assert retrieved_contract.remaining_amount == 5000.0
    assert retrieved_contract.status == False

# Test 2 : Vérification des champs obligatoires
def test_contract_missing_required_fields(session, client, sales_contact):
    # Tenter de créer un contrat sans montant (amount)
    contract = Contract(
        client=client,
        sales_contact=sales_contact,
        remaining_amount=5000.0,
        status=False
    )
    session.add(contract)
    with pytest.raises(IntegrityError):
        session.commit()

# # Test 3 : Vérification de la Contrainte de Clé Étrangère sur client_id
def test_contract_invalid_client_id(session, sales_contact):
    # Tenter de créer un contrat avec un client_id inexistant
    contract = Contract(
        client_id=999,
        sales_contact=sales_contact,
        amount=10000.0,
        remaining_amount=5000.0,
        status=False
    )
    session.add(contract)
    with pytest.raises(IntegrityError):
        session.commit()


# Test 4 : Vérification de la Relation avec Event
def test_contract_event_relationship(session, client, sales_contact):
    # Créer un contrat
    contract = Contract(
        client=client,
        sales_contact=sales_contact,
        amount=20000.0,
        remaining_amount=10000.0,
        status=True
    )
    session.add(contract)
    session.commit()

    # Importer le modèle Event
    from models.event import Event

    # Créer un département et un support_contact
    support_department = Department(name='Support', description='Support department')
    session.add(support_department)
    session.commit()

    support_contact = User(
        username='supportuser',
        hashed_password='hashedpassword',
        fullname='Support User',
        email='supportuser@example.com',
        phone='0987654321',
        department=support_department
    )
    session.add(support_contact)
    session.commit()

    # Créer un événement associé au contrat
    event = Event(
        name='Test Event',
        contract=contract,
        support_contact=support_contact,
        location='Test Location',
        attendees=50,
        event_date_start=datetime(2023, 1, 1, 10, 0, 0),
        event_date_end=datetime(2023, 1, 1, 18, 0, 0),
        notes='Test notes'
    )
    session.add(event)
    session.commit()

    # Vérifier que l'événement est associé au contrat
    assert len(contract.events) == 1
    assert contract.events[0].name == 'Test Event'

