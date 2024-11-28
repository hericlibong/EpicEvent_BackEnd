import pytest
from sqlalchemy import create_engine
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

    yield session
    session.close()
    # transaction.rollback()
    connection.close()

@pytest.fixture(scope='function')
def department(session):
    department = Department(name='Commercial', description='Commercial department')
    session.add(department)
    session.commit()
    return department

@pytest.fixture(scope='function')
def sales_contact(session, department):
    user = User(
        username='salesrep',
        hashed_password='hashedpassword',
        fullname='Sales Representative',
        email='salesrep@example.com',
        phone='0123456789',
        department=department
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

@pytest.fixture(scope='function')
def contract(session, client, sales_contact):
    contract = Contract(
        client=client,
        sales_contact=sales_contact,
        amount=10000.0,
        remaining_amount=5000.0,
        status=True
    )
    session.add(contract)
    session.commit()
    return contract

@pytest.fixture(scope='function')
def support_department(session):
    department = Department(name='Support', description='Support department')
    session.add(department)
    session.commit()
    return department

@pytest.fixture(scope='function')
def support_contact(session, support_department):
    user = User(
        username='supportuser',
        hashed_password='hashedpassword',
        fullname='Support User',
        email='supportuser@example.com',
        phone='0987654321',
        department=support_department
    )
    session.add(user)
    session.commit()
    return user


# Test 1 : Création d'un Événement
def test_create_event(session, contract, support_contact):
    # Crée un client
    event = Event(
        name='Annual Conference',
        contract=contract,
        support_contact=support_contact,
        location='Virtual space',
        attendees=100,
        event_date_start=datetime(2021, 10, 1, 8, 0),
        event_date_end=datetime(2021, 10, 2, 17, 0),
        notes='Annual conference for the company'
    )
    session.add(event)
    session.commit()

    # Vérifie que l'événement a bien été créé
    created_event = session.query(Event).filter_by(name='Annual Conference').one()
    assert created_event.location == 'Virtual space'
    assert created_event.attendees == 100
    assert created_event.notes == 'Annual conference for the company'
    assert created_event.contract.id == contract.id
    assert created_event.support_contact.username == 'supportuser'

# Test 2 : Vérification des Champs Obligatoires
def test_event_missing_required_fields(session, contract, support_contact):

    # Tenter de créer un événement sans nom
    event = Event(
        # name manquant
        contract=contract,
        support_contact=support_contact,
        location='Conference Hall A',
        attendees=200,
        event_date_start=datetime(2023, 5, 10, 9, 0, 0),
        event_date_end=datetime(2023, 5, 10, 17, 0, 0),
        notes='Missing name field.'
    )
    session.add(event)
    with pytest.raises(IntegrityError):
        session.commit()

# Test 3 : Vérification de la Contrainte de Clé Étrangère sur contract_id
# def test_event_invalid_contract(session, support_contact):
#     from sqlalchemy.exc import IntegrityError
#     from datetime import datetime
#     from models.event import Event

#     # Tenter de créer un événement avec un contract_id inexistant
#     event = Event(
#         name='Invalid Contract Event',
#         contract_id=999,  # ID inexistant
#         support_contact=support_contact,
#         location='Conference Hall B',
#         attendees=100,
#         event_date_start=datetime(2023, 6, 15, 10, 0, 0),
#         event_date_end=datetime(2023, 6, 15, 16, 0, 0),
#         notes='Event with invalid contract_id.'
#     )
#     session.add(event)
#     with pytest.raises(IntegrityError):
#         session.commit()

