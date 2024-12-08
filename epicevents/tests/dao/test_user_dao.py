import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base
from models.user import User
from models.department import Department
from dao.user_dao import UserDAO
from unittest.mock import patch

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
def user_dao(session):
    dao = UserDAO()
    dao.session = session
    return dao

@pytest.fixture(scope="function")
def sample_department(session):
    department = Department(name="IT", description="IT Department")
    session.add(department)
    session.commit()
    return department

def test_create_user(user_dao, sample_department):
    """
    Teste la création d'un utilisateur avec user_dao et sample_department.
    """
    user_data = {
        "username": "testuser",
        "hashed_password": "hashedpassword",
        "fullname": "Test User",
        "email": "testuser@example.com",
        "phone": "1234567890",
        "department_id": sample_department.id
    }
    user = user_dao.create_user(user_data)
    assert user.id is not None
    assert user.username == "testuser"
    assert user.department.name == "IT"

def test_get_user_by_id(user_dao, session, sample_department):
    """
    Teste la récupération d'un utilisateur par son identifiant.
    """
    user = User(username="testuser",
                hashed_password="hashedpassword",
                fullname="Test User",
                email="testuser@example.com",
                phone="1234567890",
                department_id=sample_department.id)
    session.add(user)
    session.commit()

    retrieved_user = user_dao.get_user_by_id(user.id)
    assert retrieved_user is not None
    assert retrieved_user.username == "testuser"

def test_update_user(user_dao, session, sample_department):
    """
    Teste la mise à jour des informations d'un utilisateur dans la base de données.
    """
    user = User(username="testuser",
                hashed_password="hashedpassword",
                fullname="Test User",
                email="testuser@example.com",
                phone="1234567890",
                department_id=sample_department.id)
    session.add(user)
    session.commit()

    updated_data = {"fullname": "Updated User", "phone": "0987654321"}
    updated_user = user_dao.update_user(user.id, updated_data)
    assert updated_user.fullname == "Updated User"
    assert updated_user.phone == "0987654321"

# Test de la méthode update_user avec un ID inexistant
def test_update_user_none(user_dao, session, sample_department):
    """
    Teste la mise à jour d'un utilisateur et la gestion des ID inexistants.
    """
    # Créer un utilisateur
    user_data = {
        "username": "testuser",
        "hashed_password": "hashedpassword",
        "fullname": "Test User",
        "email": "testuser@example.com",
        "phone": "1234567890",
        "department": sample_department
    }
    user = User(**user_data)
    session.add(user)
    session.commit()

    # Mettre à jour l'utilisateur
    updated_data = {"fullname": "Updated User", "email": "updated@example.com"}
    updated_user = user_dao.update_user(user.id, updated_data)

    # Vérifier les mises à jour
    assert updated_user is not None
    assert updated_user.fullname == "Updated User"
    assert updated_user.email == "updated@example.com"

    # Tester un ID utilisateur inexistant
    non_existent_update = user_dao.update_user(9999, updated_data)
    assert non_existent_update is None

def test_delete_user(user_dao, session, sample_department):
    """
    Teste la suppression d'un utilisateur.
    """
    user = User(username="testuser",
                hashed_password="hashedpassword",
                fullname="Test User",
                email="testuser@example.com",
                phone="1234567890",
                department_id=sample_department.id)
    session.add(user)
    session.commit()

    is_deleted = user_dao.delete_user(user.id)
    assert is_deleted
    assert user_dao.get_user_by_id(user.id) is None

# Test de la méthode delete_user avec un ID inexistant
def test_delete_user_id_none(user_dao, session, sample_department):
    """
    Teste la suppression d'un utilisateur avec un ID valide et un ID inexistant.
    """
    # Créer un utilisateur
    user_data = {
        "username": "testuser",
        "hashed_password": "hashedpassword",
        "fullname": "Test User",
        "email": "testuser@example.com",
        "phone": "1234567890",
        "department": sample_department
    }
    user = User(**user_data)
    session.add(user)
    session.commit()

    # Supprimer l'utilisateur
    delete_success = user_dao.delete_user(user.id)
    assert delete_success is True

    # Vérifier que l'utilisateur n'existe plus
    assert user_dao.get_user_by_id(user.id) is None

    # Tester une suppression avec un ID inexistant
    delete_nonexistent = user_dao.delete_user(9999)
    assert delete_nonexistent is False

# Test de la méthode get_user_by_username
def test_get_user_by_username(user_dao, session, sample_department):
    """
    Teste la récupération d'un utilisateur par son nom d'utilisateur.
    """
    # Créer un utilisateur
    user_data = {
        "username": "testuser",
        "hashed_password": "hashedpassword",
        "fullname": "Test User",
        "email": "testuser@example.com",
        "phone": "1234567890",
        "department": sample_department
    }
    user = User(**user_data)
    session.add(user)
    session.commit()

    # Tester la récupération par nom d'utilisateur
    retrieved_user = user_dao.get_user_by_username("testuser")
    assert retrieved_user is not None
    assert retrieved_user.username == "testuser"
    assert retrieved_user.email == "testuser@example.com"

# Test de la méthode get_all_users
def test_get_all_users(user_dao, session, sample_department):
    """
    Teste la récupération de tous les utilisateurs depuis la base de données.
    """
    # Créer plusieurs utilisateurs
    users_data = [
        {
            "username": "user1",
            "hashed_password": "password1",
            "fullname": "User One",
            "email": "user1@example.com",
            "phone": "1234567891",
            "department": sample_department
        },
        {
            "username": "user2",
            "hashed_password": "password2",
            "fullname": "User Two",
            "email": "user2@example.com",
            "phone": "1234567892",
            "department": sample_department
        }
    ]
    for user_data in users_data:
        session.add(User(**user_data))
    session.commit()

    # Tester la récupération de tous les utilisateurs
    all_users = user_dao.get_all_users()
    assert len(all_users) == 2
    assert {user.username for user in all_users} == {"user1", "user2"}

# Test de la méthode get_user_by_email
def test_get_user_by_email(user_dao, session, sample_department):
    """
    Teste la récupération d'un utilisateur par email.
    """
    # Créer un utilisateur
    user_data = {
        "username": "testuser",
        "hashed_password": "hashedpassword",
        "fullname": "Test User",
        "email": "testuser@example.com",
        "phone": "1234567890",
        "department": sample_department
    }
    user = User(**user_data)
    session.add(user)
    session.commit()

    # Tester la récupération par email
    retrieved_user = user_dao.get_user_by_email("testuser@example.com")
    assert retrieved_user is not None
    assert retrieved_user.username == "testuser"
    assert retrieved_user.email == "testuser@example.com"

# Test du logger dans UserDAO
def test_user_dao_logger_initialization(user_dao):
    """
    Teste si le logger est correctement initialisé dans UserDAO.
    """
    assert user_dao.logger is not None
    assert user_dao.logger.name == 'epicevents.dao'



def test_create_user_exception(user_dao, sample_department):
    """
    Teste si une exception lors de la création d'un utilisateur est bien capturée.
    """
    with patch.object(user_dao.session, 'commit', side_effect=RuntimeError("Test RuntimeError")):
        with pytest.raises(RuntimeError) as exc_info:
            user_dao.create_user({
                "username": "testuser",
                "hashed_password": "hashedpassword",
                "fullname": "Test User",
                "email": "testuser@example.com",
                "phone": "1234567890",
                "department_id": sample_department.id
            })
        assert "Test RuntimeError" in str(exc_info.value)

def test_update_user_exception(user_dao, session, sample_department):
    """
    Teste si une exception lors de la mise à jour d'un utilisateur est bien capturée.
    """
    user = User(username="testuser",
                hashed_password="hashedpassword",
                fullname="Test User",
                email="testuser@example.com",
                phone="1234567890",
                department_id=sample_department.id)
    session.add(user)
    session.commit()

    with patch.object(user_dao.session, 'commit', side_effect=ValueError("Test ValueError")):
        with pytest.raises(ValueError) as exc_info:
            user_dao.update_user(user.id, {"fullname": "Updated User"})
        assert "Test ValueError" in str(exc_info.value)
