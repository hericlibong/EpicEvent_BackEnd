import pytest
from unittest.mock import MagicMock
from controllers.event_controller import EventController
from models.event import Event
from models.contract import Contract
from models.client import Client
from models.user import User
from datetime import datetime

@pytest.fixture
def mock_event_dao():
    """
    Mock pour EventDAO
    """
    dao = MagicMock()
    return dao

@pytest.fixture
def event_controller(mock_event_dao):
    """
    Controller initialisé avec le DAO mocké
    """
    controller = EventController()
    controller.event_dao = mock_event_dao
    return controller

@pytest.fixture
def sample_event():
    """
    Événement simulé pour les tests
    """
    client = Client(id=1, fullname="Test Client", email="testclient@example.com", phone="123456789", company_name="Test Company")
    contract = Contract(id=1, client_id=1, sales_contact_id=2, status=True, amount=5000, remaining_amount=2500)
    support_user = User(id=3, username="supportuser", fullname="Support User", email="supportuser@example.com", phone="987654321")
    event = Event(
        id=1,
        contract_id=contract.id,
        support_contact_id=support_user.id,
        name="Sample Event",
        event_date_start=datetime(2023, 1, 1, 10, 0),
        event_date_end=datetime(2023, 1, 1, 18, 0),
        location="Test Location",
        attendees=100,
        notes="This is a sample event."
    )
    return event

# 1. Test de la méthode get_all_events
def test_get_all_events_no_events(event_controller, mock_event_dao):
    mock_event_dao.get_all_events.return_value = []
    events = event_controller.get_all_events()
    assert events == []
    mock_event_dao.get_all_events.assert_called_once()

def test_get_all_events_with_events(event_controller, mock_event_dao, sample_event):
    mock_event_dao.get_all_events.return_value = [sample_event]
    events = event_controller.get_all_events()
    assert events == [sample_event]
    mock_event_dao.get_all_events.assert_called_once()

# 2. Test de la méthode create_event
def test_create_event_success(event_controller, mock_event_dao, sample_event):
    mock_event_dao.create_event.return_value = sample_event
    event_data = {"name": "Sample Event"}
    event = event_controller.create_event(event_data)
    assert event == sample_event
    mock_event_dao.create_event.assert_called_once_with(event_data)

def test_create_event_failure(event_controller, mock_event_dao):
    mock_event_dao.create_event.side_effect = Exception("Erreur de création")
    event_data = {"name": "Sample Event"}
    event = event_controller.create_event(event_data)
    assert event is None
    mock_event_dao.create_event.assert_called_once_with(event_data)

# 3. Test de la méthode get_event_by_id
def test_get_event_by_id_not_found(event_controller, mock_event_dao):
    mock_event_dao.get_event_by_id.return_value = None
    event = event_controller.get_event_by_id(1)
    assert event is None
    mock_event_dao.get_event_by_id.assert_called_once_with(1)

def test_get_event_by_id_found(event_controller, mock_event_dao, sample_event):
    mock_event_dao.get_event_by_id.return_value = sample_event
    event = event_controller.get_event_by_id(1)
    assert event == sample_event
    mock_event_dao.get_event_by_id.assert_called_once_with(1)

# 4. Test de la méthode update_event
def test_update_event_success(event_controller, mock_event_dao, sample_event):
    mock_event_dao.update_event.return_value = sample_event
    event_data = {"name": "Updated Event"}
    event = event_controller.update_event(1, event_data)
    assert event == sample_event
    mock_event_dao.update_event.assert_called_once_with(1, event_data)

def test_update_event_not_found(event_controller, mock_event_dao):
    mock_event_dao.update_event.return_value = None
    event_data = {"name": "Updated Event"}
    event = event_controller.update_event(1, event_data)
    assert event is None
    mock_event_dao.update_event.assert_called_once_with(1, event_data)

def test_update_event_failure(event_controller, mock_event_dao):
    mock_event_dao.update_event.side_effect = Exception("Erreur de mise à jour")
    event_data = {"name": "Updated Event"}
    event = event_controller.update_event(1, event_data)
    assert event is None
    mock_event_dao.update_event.assert_called_once_with(1, event_data)

# 5. Test de la méthode assign_support
def test_assign_support_success(event_controller, mock_event_dao, sample_event):
    mock_event_dao.assign_support.return_value = sample_event
    event = event_controller.assign_support(1, 3)
    assert event == sample_event
    mock_event_dao.assign_support.assert_called_once_with(1, 3)

def test_assign_support_not_found(event_controller, mock_event_dao):
    mock_event_dao.assign_support.return_value = None
    event = event_controller.assign_support(1, 3)
    assert event is None
    mock_event_dao.assign_support.assert_called_once_with(1, 3)

# 6. Test de la méthode get_events_by_support
def test_get_events_by_support_no_events(event_controller, mock_event_dao):
    mock_event_dao.get_events_by_support.return_value = []
    events = event_controller.get_events_by_support(3)
    assert events == []
    mock_event_dao.get_events_by_support.assert_called_once_with(3)

def test_get_events_by_support_with_events(event_controller, mock_event_dao, sample_event):
    mock_event_dao.get_events_by_support.return_value = [sample_event]
    events = event_controller.get_events_by_support(3)
    assert events == [sample_event]
    mock_event_dao.get_events_by_support.assert_called_once_with(3)

# 7. Test de la méthode close
def test_close(event_controller, mock_event_dao):
    event_controller.close()
    mock_event_dao.close.assert_called_once()
