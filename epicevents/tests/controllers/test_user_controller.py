import pytest
from unittest.mock import MagicMock, patch
from utils.security import hash_password, create_access_token, verify_password, verify_access_token
from controllers.user_controller import UserController
from models.user import User
from models.department import Department

@pytest.fixture
def mock_user_dao():
    dao = MagicMock()
    return dao

@pytest.fixture
def user_controller(mock_user_dao):
    controller = UserController()
    controller.user_dao = mock_user_dao
    return controller

# Teste l'enregistrement réussi d'un utilisateur
def test_register_user_success(user_controller, mock_user_dao):
    mock_user_dao.get_user_by_username.return_value = None
    mock_user_dao.get_user_by_email.return_value = None
    mock_user_dao.create_user.return_value = User(id=1, username="newuser", email="newuser@example.com")

    user_data = {
        "username": "newuser",
        "password": "securepassword",
        "email": "newuser@example.com",
        "department_id": 1,
    }
    user = user_controller.register_user(user_data)
    assert user is not None
    assert user.username == "newuser"

# Teste l'échec de l'enregistrement d'un utilisateur avec un nom d'utilisateur existant
def test_register_user_existing_username(user_controller, mock_user_dao):
    mock_user_dao.get_user_by_username.return_value = User(username="existinguser")
    user_data = {
        "username": "existinguser",
        "password": "securepassword",
        "email": "test@exemple.com",
        "department_id": 1,
    }
    user = user_controller.register_user(user_data)
    assert user is None

# Teste l'échec de l'enregistrement d'un utilisateur avec une adresse email existante
def test_register_user_existing_email(user_controller, mock_user_dao):
    mock_user_dao.get_username.return_value = None
    mock_user_dao.get_user_by_email.return_value = User(email="test@exemple.com")
    user_data = {
        "username": "newuser",
        "password": "securepassword",
        "email": "test@exemple.com",
        "department_id": 1,
    }
    user = user_controller.register_user(user_data)
    assert user is None

# Teste l'échec à cause d'un département manquant
def test_register_user_missing_department(user_controller, mock_user_dao):
    mock_user_dao.get_user_by_username.return_value = None
    mock_user_dao.get_user_by_email.return_value = None
    user_data = {"username": "newuser", 
                 "password": "password", 
                 "email": "test@example.com"
            }
    user = user_controller.register_user(user_data)
    assert user is None

# Teste une connexion réussie
def test_login_user_success(user_controller, mock_user_dao):
    user = User(id=1, username="testuser", hashed_password=hash_password("password"), department=Department(name="Test Department"))
    mock_user_dao.get_user_by_username.return_value = user
    token, returned_user = user_controller.login_user("testuser", "password")
    assert token is not None
    assert returned_user.username == "testuser"

# Teste l'échec à cause d'un utilisateur introuvable
def test_login_user_not_found(user_controller, mock_user_dao):
    mock_user_dao.get_user_by_username.return_value = None
    token, error = user_controller.login_user("nonexistent", "password")
    assert token is None
    assert error == "Utilisateur non trouvé."

# Teste l'échec à cause d'un mot de passe incorrect
def test_login_user_wrong_password(user_controller, mock_user_dao):
    user = User(id=1, username="testuser", hashed_password=hash_password("password"), department=Department(name="Test Department"))
    mock_user_dao.get_user_by_username.return_value = user
    token, error = user_controller.login_user("testuser", "wrongpassword")
    assert token is None
    assert error == "Mot de passe incorrect."

# Teste la récupération d'un utilisateur existant
def test_get_user_success(user_controller, mock_user_dao):
    mock_user_dao.get_user_by_id.return_value = User(id=1, username="testuser")
    user = user_controller.get_user(1)
    assert user is not None
    assert user.username == "testuser"

# Teste un utilisateur introuvable
def test_get_user_not_found(user_controller, mock_user_dao):
    mock_user_dao.get_user_by_id.return_value = None
    user = user_controller.get_user(999)
    assert user is None

# Teste la récupération de la liste des utilisateurs
def test_get_users_list(user_controller, mock_user_dao):
    users = [User(id=1, username="user1"), User(id=2, username="user2")]
    mock_user_dao.get_all_users.return_value = users
    user_list = user_controller.get_users_list()
    assert len(user_list) == 2
    assert user_list[0].username == "user1"

# Teste une liste vide
def test_get_users_list_empty(user_controller, mock_user_dao):
    mock_user_dao.get_all_users.return_value = []
    user_list = user_controller.get_users_list()
    assert user_list == []

# Teste une mise à jour réussie
def test_update_user_success(user_controller, mock_user_dao):
    mock_user_dao.update_user.return_value = User(id=1, username="updateduser")
    user_data = {"username": "updateduser"}
    user = user_controller.update_user(1, user_data)
    assert user is not None
    assert user.username == "updateduser"

# Teste une mise à jour échouée
def test_update_user_not_found(user_controller, mock_user_dao):
    mock_user_dao.update_user.return_value = None
    user_data = {"username": "updateduser"}
    user = user_controller.update_user(999, user_data)
    assert user is None

# Teste une suppression réussie
def test_delete_user_success(user_controller, mock_user_dao):
    mock_user_dao.delete_user.return_value = True
    result = user_controller.delete_user(1)
    assert result is None  # Suppression réussie, mais la méthode ne retourne rien

# Teste une suppression échouée
def test_delete_user_not_found(user_controller, mock_user_dao):
    mock_user_dao.delete_user.return_value = False
    result = user_controller.delete_user(999)
    assert result is None  # Suppression échouée, mais la méthode ne retourne rien

# Teste la vérification d'un token valide
def test_verify_token_success(user_controller):
    valid_token = create_access_token({"user_id": 1, "username": "testuser"})
    result = user_controller.verify_token(valid_token)
    assert result["username"] == "testuser"

# Teste la vérification d'un token invalide
def test_verify_token_invalid(user_controller):
    invalid_token = "invalid.token.here"
    result = user_controller.verify_token(invalid_token)
    assert result is None

def test_verify_token_valid(user_controller):
    # Données utilisateur simulées
    token_data = {"user_id": 1, "username": "testuser", "department": "Test Department"}

    # Mock de verify_access_token
    with patch("controllers.user_controller.verify_access_token", return_value=token_data):
        result = user_controller.verify_token("valid_token")
        assert result == token_data

def test_verify_token_invalid(user_controller):
    # Mock de verify_access_token pour lever une exception
    with patch("controllers.user_controller.verify_access_token", side_effect=Exception("Invalid token")):
        result = user_controller.verify_token("invalid_token")
        assert result is None

def test_register_user_existing_email(user_controller, mock_user_dao):
    """
    Teste l'échec d'enregistrement lorsqu'un email est déjà utilisé.
    """
    # Simule un utilisateur inexistant pour le username
    mock_user_dao.get_user_by_username.return_value = None

    # Simule un utilisateur existant pour l'email
    mock_user_dao.get_user_by_email.return_value = User(email="existing@example.com")

    # Données utilisateur de test
    user_data = {
        "username": "newuser",
        "password": "password",
        "email": "existing@example.com",
        "department_id": 1
    }
    # Appelle la méthode et vérifie le retour
    user = user_controller.register_user(user_data)
    assert user is None

# Teste la fermeture de session
def test_close_user_controller(user_controller, mock_user_dao):
    # Appeler la méthode close
    user_controller.close()
    # Vérifier que mock_user_dao.close a été appelé
    mock_user_dao.close.assert_called_once()
