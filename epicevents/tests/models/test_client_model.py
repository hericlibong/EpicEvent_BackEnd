import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base
from models.client import Client
from models.user import User
from models.department import Department
from models.contract import Contract
from sqlalchemy.exc import IntegrityError

@pytest.fixture(scope='module')
def test_engine():
    # Base de données SQLite en mémoire
    engine = create_engine('sqlite:///:memory:')
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

    # Nettoie la base de données après chaque test
    session.close()
    # transaction.rollback()
    connection.close()

# Test 1 : tester la création d'un client
def test_create_client(session):
    # Créer un département pour le Commercial
    department = Department(name='Commercial', description='Commercial department')
    session.add(department)
    session.commit()

    # Créer un utilisateur pour le Commercial
    sales_contact = User(
        username='salesrep',
        hashed_password='hashedpassword',
        fullname='Sales Representative',
        email='salesrep@email.com',
        phone='1234567890',
        department=department
    )
    session.add(sales_contact)
    session.commit()

    # Client associé au commercial
    client = Client(
        fullname='Client Fullname',
        email = 'client@email.com',
        phone='1234567890',
        company_name='Client Company',
        sales_contact=sales_contact
    )
    session.add(client)
    session.commit()    

    created_client = session.query(Client).filter_by(email='client@email.com').one()
    assert created_client.fullname == 'Client Fullname'
    assert created_client.sales_contact.username == 'salesrep'
    assert created_client.company_name == 'Client Company'


# Test 2 : Tester l'unicité de l'email du client
def test_client_email_uniqueness(session):
    # Créer un département et un commercial comme précédemment
    department = Department(name='Commercial', description='Commercial department')
    session.add(department)
    session.commit()

    sales_contact = User(
        username='salesrep2',
        hashed_password='hashedpassword',
        fullname='Sales Rep 2',
        email='salesrep2@example.com',
        phone='0123456789',
        department=department
    )
    session.add(sales_contact)
    session.commit()

    # Créer un client avec un email unique
    client1 = Client(
        fullname='Jane Smith',
        email='janesmith@example.com',
        phone='1231231234',
        company_name='Smith Co',
        sales_contact=sales_contact
    )
    session.add(client1)
    session.commit()

    # Tenter de créer un autre client avec le même email
    client2 = Client(
        fullname='Jane Doe',
        email='janesmith@example.com',  # Même email que client1
        phone='3213214321',
        company_name='Doe Co',
        sales_contact=sales_contact
    )
    session.add(client2)
    with pytest.raises(IntegrityError):
        session.commit()

# Test 3 : Champs obligatoires

def test_client_missing_required_fields(session):
    # Créer un département et un commercial
    department = Department(name='Commercial', description='Commercial department')
    session.add(department)
    session.commit()

    sales_contact = User(
        username='salesrep3',
        hashed_password='hashedpassword',
        fullname='Sales Rep 3',
        email='salesrep3@example.com',
        phone='0123456789',
        department=department
    )
    session.add(sales_contact)
    session.commit()

    # Tenter de créer un client sans email (champ obligatoire)
    client = Client(
        fullname='No Email Client',
        email=None,  # Email manquant
        phone='5555555555',
        company_name='No Email Co',
        sales_contact=sales_contact
    )
    session.add(client)
    with pytest.raises(IntegrityError):
        session.commit()

# Test 4 : Vérification de la Relation avec Contract

def test_client_contract_relationship(session):
    # Créer un département et un commercial
    department = Department(name='Commercial', description='Commercial department')
    session.add(department)
    session.commit()

    sales_contact = User(
        username='salesrep4',
        hashed_password='hashedpassword',
        fullname='Sales Rep 4',
        email='salesrep4@example.com',
        phone='0123456789',
        department=department
    )
    session.add(sales_contact)
    session.commit()

    # Créer un client
    client = Client(
        fullname='Contract Client',
        email='contractclient@example.com',
        phone='6666666666',
        company_name='Contract Co',
        sales_contact=sales_contact
    )
    session.add(client)
    session.commit()

    # Importer le modèle Contract
    

    # Créer un contrat pour ce client
    contract = Contract(
        client=client,
        sales_contact=sales_contact,
        amount=10000.0,
        remaining_amount=5000.0,
        status=False
    )
    session.add(contract)
    session.commit()

    # Vérifier que le contrat est associé au client
    assert len(client.contracts) == 1
    assert client.contracts[0].amount == 10000.0




