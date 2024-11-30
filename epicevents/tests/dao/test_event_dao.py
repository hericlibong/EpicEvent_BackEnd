import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base
from models.event import Event
from models.contract import Contract
from models.client import Client
from models.user import User
from models.department import Department
from dao.event_dao import EventDAO
from datetime import datetime

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
def event_dao(session):
    dao = EventDAO()
    dao.session = session
    return dao

@pytest.fixture(scope="function")
def sample_contract_and_support_contact(session):
    department = Department(name="Support", description="Support Department")
    session.add(department)
    session.commit()

    support_contact = User(username="supportuser",
                           hashed_password="hashedpassword",
                           fullname="Support User",
                           email="supportuser@example.com",
                           phone="1234567890",
                           department_id=department.id)
    session.add(support_contact)
    session.commit()

    client = Client(fullname="Test Client",
                    email="testclient@example.com",
                    phone="0987654321",
                    company_name="Test Company",
                    sales_contact_id=support_contact.id)
    session.add(client)
    session.commit()

    contract = Contract(client_id=client.id,
                        sales_contact_id=support_contact.id,
                        status=True,
                        amount=10000.0,
                        remaining_amount=5000.0)
    session.add(contract)
    session.commit()

    return contract, support_contact

def test_create_event(event_dao, sample_contract_and_support_contact):
    contract, support_contact = sample_contract_and_support_contact
    event_data = {
        "contract_id": contract.id,
        "support_contact_id": support_contact.id,
        "name": "Test Event",
        "event_date_start": datetime(2021, 10, 1, 8, 0),
        "event_date_end": datetime(2021, 10, 2, 17, 0),
        "location": "Test Location",
        "attendees": 50,
        "notes": "Test Notes"
    }
    event = event_dao.create_event(event_data)
    assert event.id is not None
    assert event.name == "Test Event"
    assert event.location == "Test Location"
    assert event.contract.client.fullname == "Test Client"

def test_get_event_by_id(event_dao, session, sample_contract_and_support_contact):
    contract, support_contact = sample_contract_and_support_contact
    event = Event(contract_id=contract.id,
                  support_contact_id=support_contact.id,
                    name="Test Event",
                  event_date_start=datetime(2021, 10, 1, 8, 0),
                  event_date_end=datetime(2021, 10, 2, 17, 0),
                  location="Test Location",
                  attendees=50,
                  notes="Test Notes")
    session.add(event)
    session.commit()

    retrieved_event = event_dao.get_event_by_id(event.id)
    assert retrieved_event is not None
    assert retrieved_event.location == "Test Location"

def test_get_all_events(event_dao, session, sample_contract_and_support_contact):
    contract, support_contact = sample_contract_and_support_contact
    event1 = Event(contract_id=contract.id,
                   support_contact_id=support_contact.id,
                   name = "Event 1",
                   event_date_start=datetime(2021, 10, 1, 8, 0),
                   event_date_end=datetime(2021, 10, 2, 17, 0),
                   location="Location 1",
                   attendees=50,
                   notes="Notes 1")
    event2 = Event(contract_id=contract.id,
                   support_contact_id=support_contact.id,
                   name = "Event 2",
                   event_date_start=datetime(2021, 10, 1, 8, 0),
                   event_date_end=datetime(2021, 10, 2, 17, 0),
                   location="Location 2",
                   attendees=30,
                   notes="Notes 2")
    session.add_all([event1, event2])
    session.commit()

    events = event_dao.get_all_events()
    assert len(events) == 2
    assert events[0].location in ["Location 1", "Location 2"]

def test_update_event(event_dao, session, sample_contract_and_support_contact):
    contract, support_contact = sample_contract_and_support_contact
    event = Event(contract_id=contract.id,
                  support_contact_id=support_contact.id,
                  name="Test Event",
                  event_date_start=datetime(2021, 10, 1, 8, 0),
                   event_date_end=datetime(2021, 10, 2, 17, 0),
                  location="Test Location",
                  attendees=50,
                  notes="Test Notes")
    session.add(event)
    session.commit()

    updated_data = {"location": "Updated Location", "attendees": 100}
    updated_event = event_dao.update_event(event.id, updated_data)
    assert updated_event.location == "Updated Location"
    assert updated_event.attendees == 100

def test_delete_event(event_dao, session, sample_contract_and_support_contact):
    contract, support_contact = sample_contract_and_support_contact
    event = Event(contract_id=contract.id,
                  support_contact_id=support_contact.id,
                  name="Test Event",
                  event_date_start=datetime(2021, 10, 1, 8, 0),
                   event_date_end=datetime(2021, 10, 2, 17, 0),
                  location="Test Location",
                  attendees=50,
                  notes="Test Notes")
    session.add(event)
    session.commit()

    is_deleted = event_dao.delete_event(event.id)
    assert is_deleted
    assert event_dao.get_event_by_id(event.id) is None
