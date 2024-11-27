import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base
from models.user import User
from models.department import Department

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

    yield session # Exécute les tests

    # Nettoie la base de données après chaque test
    session.close()
    # transaction.rollback()
    connection.close()

def test_create_user(session):
    # test de création d'un utilisateur

    # Crée un département
    department = Department(name='Commercial', description='Commercial department')
    session.add(department)
    session.commit()

    user = User(username='testuser',
                hashed_password='hashedpassword',
                fullname='Test User',
                email='testuser@email.com', 
                phone='1234567890', 
                department=department
                )
    session.add(user)
    session.commit()

    # Vérifie que l'utilisateur a bien été créé
    created_user = session.query(User).filter_by(username='testuser').one()
    assert created_user.fullname == 'Test User'
    assert created_user.email == 'testuser@email.com'
    assert created_user.department.name == 'Commercial'
    assert created_user.department.description == 'Commercial department'

def test_user_repr(session):
    # test de la représentation d'un utilisateur
    
    from models.department import Department

    # Crée un département
    department = Department(name='Commercial', description='Commercial department')
    session.add(department)
    session.commit()

    user = User(username='testuser',
                hashed_password='hashedpassword',
                fullname='Test User',
                email='testuser@email.com', 
                phone='1234567890', 
                department=department
                )
    session.add(user)
    session.commit()

    # Vérifie que l'utilisateur a bien été créé
    created_user = session.query(User).filter_by(username='testuser').one()
    assert created_user.fullname == 'Test User'
    assert created_user.email == 'testuser@email.com'
    assert created_user.department.name == 'Commercial'
    assert created_user.department.description == 'Commercial department'

    # Teste la représentation de l'utilisateur
    user_repr = repr(created_user)
    assert user.username in user_repr
    assert user.department.name in user_repr



