import pytest
import os
import sys

# Définir la variable d'environnement pour utiliser une base de données en mémoire
os.environ['DATABASE_URL'] = 'sqlite:///:memory:'

import config
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from models.base import Base
from models.department import Department
from models.user import User
from dao.user_dao import UserDAO

@pytest.fixture(scope='session')
def test_engine():
    """Crée un moteur de base de données de test"""
    engine = create_engine('sqlite:///:memory:', echo=False)
    
    # Créer toutes les tables
    Base.metadata.create_all(bind=engine)
    
    return engine

@pytest.fixture(scope='session')
def TestSessionLocal(test_engine):
    """Crée une factory de session de test"""
    return sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

@pytest.fixture(scope='function')
def session(TestSessionLocal):
    """Fournit une session de test avec gestion des transactions"""
    connection = TestSessionLocal().get_bind().connect()
    transaction = connection.begin()
    session = TestSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope='function')
def user_dao(session, monkeypatch):
    """Fournit un UserDAO configuré pour utiliser la session de test"""
    def get_test_session():
        return session
    monkeypatch.setattr(config, 'SessionLocal', get_test_session)
    return UserDAO()

@pytest.fixture(scope='function')
def department(session):
    """Crée un département de test"""
    dept = Department(name='Commercial', description='Service commercial')
    session.add(dept)
    session.commit()
    return dept

def test_create_user(user_dao, department):
    """Teste la création d'un utilisateur"""
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

# Les autres tests restent identiques...
