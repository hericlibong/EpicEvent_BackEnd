import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base
from models.client import Client
from models.user import User
from models.department import Department
from dao.client_dao import ClientDAO

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
def client_dao(session):
    dao = ClientDAO()
    dao.session = session
    return dao

@pytest.fixture(scope="function")
def sample_sales_contact(session):
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
    return sales_contact

def test_create_client(client_dao, sample_sales_contact):
    client_data = {
        "fullname": "Test Client",
        "email": "testclient@example.com",
        "phone": "0987654321",
        "company_name": "Test Company",
        "sales_contact_id": sample_sales_contact.id
    }
    client = client_dao.create_client(client_data)
    assert client.id is not None
    assert client.fullname == "Test Client"
    assert client.sales_contact.username == "salesuser"

def test_get_client_by_id(client_dao, session, sample_sales_contact):
    client = Client(fullname="Test Client",
                    email="testclient@example.com",
                    phone="0987654321",
                    company_name="Test Company",
                    sales_contact_id=sample_sales_contact.id)
    session.add(client)
    session.commit()

    retrieved_client = client_dao.get_client_by_id(client.id)
    assert retrieved_client is not None
    assert retrieved_client.email == "testclient@example.com"

def test_get_all_clients(client_dao, session, sample_sales_contact):
    client1 = Client(fullname="Client 1",
                     email="client1@example.com",
                     phone="1111111111",
                     company_name="Company 1",
                     sales_contact_id=sample_sales_contact.id)
    client2 = Client(fullname="Client 2",
                     email="client2@example.com",
                     phone="2222222222",
                     company_name="Company 2",
                     sales_contact_id=sample_sales_contact.id)
    session.add_all([client1, client2])
    session.commit()

    clients = client_dao.get_all_clients()
    assert len(clients) == 2
    assert clients[0].fullname in ["Client 1", "Client 2"]

def test_update_client(client_dao, session, sample_sales_contact):
    client = Client(fullname="Old Client",
                    email="oldclient@example.com",
                    phone="1234567890",
                    company_name="Old Company",
                    sales_contact_id=sample_sales_contact.id)
    session.add(client)
    session.commit()

    updated_data = {"fullname": "Updated Client", "phone": "0987654321"}
    updated_client = client_dao.update_client(client.id, updated_data)
    assert updated_client.fullname == "Updated Client"
    assert updated_client.phone == "0987654321"

def test_delete_client(client_dao, session, sample_sales_contact):
    client = Client(fullname="Client to Delete",
                    email="deleteclient@example.com",
                    phone="1234567890",
                    company_name="Company to Delete",
                    sales_contact_id=sample_sales_contact.id)
    session.add(client)
    session.commit()

    is_deleted = client_dao.delete_client(client.id)
    assert is_deleted
    assert client_dao.get_client_by_id(client.id) is None
