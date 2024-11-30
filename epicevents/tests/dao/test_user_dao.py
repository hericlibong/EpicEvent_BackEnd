import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base
from models.user import User
from models.department import Department
from dao.user_dao import UserDAO

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

def test_delete_user(user_dao, session, sample_department):
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
