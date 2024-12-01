import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base
from models.contract import Contract
from models.client import Client
from models.user import User
from models.department import Department
from dao.contract_dao import ContractDAO

@pytest.fixture(scope="module")
def test_engine():
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(bind=engine)
    return engine

@pytest.fixture(scope="function")
def session(test_engine):
    connection = test_engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    session = Session()

    yield session

    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def contract_dao(session):
    dao = ContractDAO()
    dao.session = session
    return dao

@pytest.fixture(scope="function")
def sample_client_and_sales_contact(session):
    department = Department(name="Sales", description="Sales Department")
    session.add(department)
    session.commit()

    sales_contact = User(username="salesuser",
                         hashed_password="hashedpassword",
                         fullname="Sales User",
                         email="salesuser@example.com",
                         phone="1234567890",
                         department_id=department.id)
    session.add(sales_contact)
    session.commit()

    client = Client(fullname="Test Client",
                    email="testclient@example.com",
                    phone="0987654321",
                    company_name="Test Company",
                    sales_contact_id=sales_contact.id)
    session.add(client)
    session.commit()

    return client, sales_contact

def test_create_contract(contract_dao, sample_client_and_sales_contact):
    client, sales_contact = sample_client_and_sales_contact
    contract_data = {
        "client_id": client.id,
        "sales_contact_id": sales_contact.id,
        "status": True,
        "amount": 10000.0,
        "remaining_amount": 5000.0
    }
    contract = contract_dao.create_contract(contract_data)
    assert contract.id is not None
    assert contract.client.fullname == "Test Client"
    assert contract.sales_contact.username == "salesuser"

def test_get_contract_by_id(contract_dao, session, sample_client_and_sales_contact):
    client, sales_contact = sample_client_and_sales_contact
    contract = Contract(client_id=client.id,
                        sales_contact_id=sales_contact.id,
                        status=True,
                        amount=10000.0,
                        remaining_amount=5000.0)
    session.add(contract)
    session.commit()

    retrieved_contract = contract_dao.get_contract_by_id(contract.id)
    assert retrieved_contract is not None
    assert retrieved_contract.client_id == client.id

def test_get_all_contracts(contract_dao, session, sample_client_and_sales_contact):
    client, sales_contact = sample_client_and_sales_contact
    contract1 = Contract(client_id=client.id,
                         sales_contact_id=sales_contact.id,
                         status=True,
                         amount=10000.0,
                         remaining_amount=5000.0)
    contract2 = Contract(client_id=client.id,
                         sales_contact_id=sales_contact.id,
                         status=False,
                         amount=20000.0,
                         remaining_amount=15000.0)
    session.add_all([contract1, contract2])
    session.commit()

    contracts = contract_dao.get_all_contracts()
    assert len(contracts) == 2
    assert contracts[0].amount in [10000.0, 20000.0]

def test_update_contract(contract_dao, session, sample_client_and_sales_contact):
    client, sales_contact = sample_client_and_sales_contact
    contract = Contract(client_id=client.id,
                        sales_contact_id=sales_contact.id,
                        status=True,
                        amount=10000.0,
                        remaining_amount=5000.0)
    session.add(contract)
    session.commit()

    updated_data = {"status": False, "remaining_amount": 2500.0}
    updated_contract = contract_dao.update_contract(contract.id, updated_data)
    assert updated_contract.status is False
    assert updated_contract.remaining_amount == 2500.0

def test_delete_contract(contract_dao, session, sample_client_and_sales_contact):
    client, sales_contact = sample_client_and_sales_contact
    contract = Contract(client_id=client.id,
                        sales_contact_id=sales_contact.id,
                        status=True,
                        amount=10000.0,
                        remaining_amount=5000.0)
    session.add(contract)
    session.commit()

    is_deleted = contract_dao.delete_contract(contract.id)
    assert is_deleted
    assert contract_dao.get_contract_by_id(contract.id) is None

# Teste la mise à jour d'un contrat et le comportement avec un ID inexistant
def test_update_contract_new(contract_dao, session, sample_client_and_sales_contact):
    """
    Teste la mise à jour d'un contrat et le comportement avec un ID inexistant.
    """
    client, sales_contact = sample_client_and_sales_contact
    # Créer un contrat
    contract = Contract(client_id=client.id,
                        sales_contact_id=sales_contact.id,
                        status=True,
                        amount=10000.0,
                        remaining_amount=5000.0)
    session.add(contract)
    session.commit()

    # Mettre à jour le contrat
    updated_data = {"status": False, "remaining_amount": 2500.0}
    updated_contract = contract_dao.update_contract(contract.id, updated_data)

    # Vérifier les mises à jour
    assert updated_contract.status is False
    assert updated_contract.remaining_amount == 2500.0

    # Tester un ID de contrat inexistant
    non_existent_update = contract_dao.update_contract(9999, updated_data)
    assert non_existent_update is None

# Teste la récupération de tous les contrats associés à un client
def test_get_contracts_by_client_id(contract_dao, session, sample_client_and_sales_contact):
    """
    Test the get_contracts_by_client_id method to retrieve contracts by client ID.
    """
    client, sales_contact = sample_client_and_sales_contact

    # Créer plusieurs contrats
    contract1 = Contract(client_id=client.id,
                         sales_contact_id=sales_contact.id,
                         status=True,
                         amount=10000.0,
                         remaining_amount=5000.0)
    contract2 = Contract(client_id=client.id,
                         sales_contact_id=sales_contact.id,
                         status=False,
                         amount=20000.0,
                         remaining_amount=15000.0)
    session.add_all([contract1, contract2])
    session.commit()

    # Tester la récupération
    contracts = contract_dao.get_contracts_by_client_id(client.id)
    assert len(contracts) == 2
    assert all(contract.client_id == client.id for contract in contracts)

# Teste la suppression d'un contrat et le comportement avec un ID inexistant
def test_delete_contract_new(contract_dao, session, sample_client_and_sales_contact):
    """
    Test the delete_contract method for removing a contract and handling non-existing IDs.
    """
    client, sales_contact = sample_client_and_sales_contact

    # Créer un contrat
    contract = Contract(client_id=client.id,
                        sales_contact_id=sales_contact.id,
                        status=True,
                        amount=10000.0,
                        remaining_amount=5000.0)
    session.add(contract)
    session.commit()

    # Tester la suppression valide
    delete_success = contract_dao.delete_contract(contract.id)
    assert delete_success is True
    assert contract_dao.get_contract_by_id(contract.id) is None

    # Tester une suppression avec un ID inexistant
    delete_invalid = contract_dao.delete_contract(9999)
    assert delete_invalid is False

# Teste la récupération de tous les contrats associés à un contact commercial
def test_get_contract_by_sales_contact(contract_dao, session, sample_client_and_sales_contact):
    """
    Test the get_contract_by_sales_contact method to retrieve all contracts by sales contact ID.
    """
    client, sales_contact = sample_client_and_sales_contact

    # Créer plusieurs contrats
    contract1 = Contract(client_id=client.id,
                         sales_contact_id=sales_contact.id,
                         status=True,
                         amount=10000.0,
                         remaining_amount=5000.0)
    contract2 = Contract(client_id=client.id,
                         sales_contact_id=sales_contact.id,
                         status=False,
                         amount=20000.0,
                         remaining_amount=15000.0)
    session.add_all([contract1, contract2])
    session.commit()

    # Tester la récupération des contrats par contact commercial
    contracts = contract_dao.get_contract_by_sales_contact(sales_contact.id)
    assert len(contracts) == 2
    assert all(contract.sales_contact_id == sales_contact.id for contract in contracts)
    assert contracts[0].client.fullname == "Test Client"  # Vérifie la relation avec le client




