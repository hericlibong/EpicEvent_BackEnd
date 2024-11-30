import pytest
import os
import sys

# Configuration de l'environnement de test
os.environ['TESTING'] = 'True'
os.environ['DATABASE_URL'] = 'sqlite:///:memory:'

import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base
from models.user import User
from models.department import Department
from models.client import Client
from models.contract import Contract
from models.event import Event
from dao.user_dao import UserDAO

# Configuration de la base de données de test
engine = create_engine('sqlite:///:memory:', echo=True)
TestSession = sessionmaker(bind=engine)

@pytest.fixture(scope='module', autouse=True)
def setup_database():
    """Configure la base de données de test"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope='function')
def session():
    """Fournit une session de test"""
    session = TestSession()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture(scope='function')
def user_dao(session, monkeypatch):
    """Configure le DAO pour utiliser la session de test"""
    def get_test_session():
        return session
    monkeypatch.setattr(config, 'SessionLocal', get_test_session)
    dao = UserDAO()
    yield dao
    session.rollback()

@pytest.fixture(scope='function')
def department(session):
    """Crée un département de test"""
    dept = Department(name='Commercial', description='Service commercial')
    session.add(dept)
    session.commit()
    return dept

def test_create_user(user_dao, department):
    """Test de la création d'un utilisateur"""
    user_data = {
        'username': 'test2user',
        'hashed_password': 'hashedpassword',
        'fullname': 'Test User',
        'email': 'testuser2@example.com',
        'phone': '0123456789',
        'department_id': department.id
    }
    user = user_dao.create_user(user_data)

    assert user.id is not None
    assert user.username == 'test2user'

    retrieved_user = user_dao.get_user_by_username('test2user')
    assert retrieved_user is not None
    assert retrieved_user.email == 'testuser2@example.com'
