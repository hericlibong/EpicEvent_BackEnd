import pytest
from unittest.mock import MagicMock
from controllers.client_controller import ClientController
from models.client import Client
from models.user import User
from models.department import Department

@pytest.fixture
def mock_client_dao():
    dao = MagicMock()
    return dao

@pytest.fixture
def client_controller(mock_client_dao):
    controller = ClientController()
    controller.client_dao = mock_client_dao
    return controller

@pytest.fixture
def sample_client():
    # Simule un client avec des données factices pour le test
    department = Department(name="Sales", description="Sales Department")
    user = User(username="salesuser", fullname="Sales User", email="sales@example.com", department=department)
    client = Client(fullname="Test Client", email="client@example.com", phone="1234567890", sales_contact_id=user.id)
    return client


# Teste la récupération de tous les clients
# 1. Tester aucun client trouvé
def test_get_all_clients_no_clients(client_controller, mock_client_dao, capsys):
    """
    Teste la récupération de clients lorsque aucun client n'est trouvé.
    """
    # Simuler que get_all_clients retourne une liste vide
    mock_client_dao.get_all_clients.return_value = []

    # Appeler la méthode du contrôleur
    clients = client_controller.get_all_clients()

    # Capturer les sorties standard (pour vérifier le print)
    captured = capsys.readouterr()

    # Vérifier que le message attendu est imprimé
    assert "Aucun client trouvé." in captured.out

    # Vérifier que la méthode retourne None
    assert clients is None

# 2. Tester la récupération de clients
def test_get_all_clients(client_controller, mock_client_dao, sample_client):
    """
    Teste la récupération de tous les clients.
    """
    # Simuler que get_all_clients retourne une liste de clients
    mock_client_dao.get_all_clients.return_value = [sample_client]

    # Appeler la méthode du contrôleur
    clients = client_controller.get_all_clients()

    # Vérifier que la méthode retourne les clients
    assert clients == [sample_client]

# 3. Test de la méthode create_client
# Scénario 1 : Création réussie
def test_create_client_success(client_controller, mock_client_dao, sample_client):
    """
    Teste la création d'un client avec succès.
    """
    # Simuler que create_client retourne le client créé
    mock_client_dao.create_client.return_value = sample_client

    # Appeler la méthode du contrôleur
    created_client = client_controller.create_client(sample_client)

    # Vérifier que le client retourné est le même que celui créé
    assert created_client == sample_client


# Scénario 2 : Email déjà utilisé (exception ValueError)
def test_create_client_failure_email(client_controller, mock_client_dao, sample_client):
    """
    Teste la création d'un client qui échoue à cause d'un email déjà utilisé.
    """
    # Simuler une exception ValueError avec le message attendu
    mock_client_dao.create_client.side_effect = ValueError("Adresse email déjà utilisée.")

    # Vérifier que l'exception est levée avec le message attendu
    with pytest.raises(ValueError, match="Adresse email déjà utilisée."):
        client_controller.create_client(sample_client)

# Scénario 3 : Erreur inattendue (exception générique)
def test_create_client_failure_generic(client_controller, mock_client_dao, sample_client):
    """
    Teste la création d'un client qui échoue à cause d'une erreur inattendue.
    """
    # Simuler une exception générique
    mock_client_dao.create_client.side_effect = Exception("Erreur inattendue.")

    # Vérifier que l'exception est levée avec le message attendu
    with pytest.raises(Exception, match="Erreur lors de la création du client"):
        client_controller.create_client(sample_client)


# Simuler que `get_client_by_id` retourne `None`.
def test_get_client_by_id_not_found(client_controller, mock_client_dao, capsys):
    """
    Teste la récupération d'un client par son identifiant lorsque le client n'est pas trouvé.
    """
    # Simuler que get_client_by_id retourne None
    mock_client_dao.get_client_by_id.return_value = None

    # Appeler la méthode du contrôleur
    client = client_controller.get_client_by_id(1)

    # Capturer les sorties standard (pour vérifier le print)
    captured = capsys.readouterr()

    # Vérifier que le message attendu est imprimé
    assert "Aucun client trouvé." in captured.out

    # Vérifier que la méthode retourne None
    assert client is None

# Scénario 2 : Client trouvé
def test_get_client_by_id_found(client_controller, mock_client_dao, sample_client):
    """
    Teste la récupération d'un client par son identifiant lorsque le client est trouvé.
    """
    # Simuler que get_client_by_id retourne un client
    mock_client_dao.get_client_by_id.return_value = sample_client

    # Appeler la méthode du contrôleur
    client = client_controller.get_client_by_id(1)

    # Vérifier que la méthode retourne le client
    assert client == sample_client

# # 5. Test de la méthode update_client
# # # Scénario 1 : Mise à jour réussie
def test_update_client_success(client_controller, mock_client_dao, sample_client):
    """
    Teste la mise à jour d'un client avec succès.
    """
    # Simuler que update_client retourne le client mis à jour
    updated_data = {"fullname": "Updated Name", "email": "updated@example.com"}
    mock_client_dao.update_client.return_value = sample_client

    # Appeler la méthode du contrôleur avec les données de mise à jour
    updated_client = client_controller.update_client(1, updated_data)

    # Vérifier que le client retourné est le même que celui mis à jour
    assert updated_client == sample_client

# # Scénario 2 : Client introuvable ou erreur lors de la mise à jour
def test_update_client_failure(client_controller, mock_client_dao, capsys):
    """
    Teste la mise à jour d'un client qui échoue à cause d'un client introuvable ou d'une erreur.
    """
    # Simuler que update_client retourne None
    mock_client_dao.update_client.return_value = None

    # Appeler la méthode du contrôleur
    updated_client = client_controller.update_client(1, {})
    # Capturer les sorties standard (pour vérifier le print)
    # Vérifier que le message attendu est imprimé
    captured = capsys.readouterr()
    assert "Aucun client trouvé ou erreur lors de la mise à jour." in captured.out
    # Vérifier que la méthode retourne None
    assert updated_client is None


def test_update_client_generic_error(client_controller, mock_client_dao):
    """
    Teste la mise à jour d'un client qui échoue à cause d'une erreur inattendue.
    """
    # Simuler une exception générique dans le DAO
    mock_client_dao.update_client.side_effect = Exception("Erreur inattendue.")

    # Vérifier que l'exception est capturée et gérée correctement
    updated_client = client_controller.update_client(1, {})
    assert updated_client is None
    
   

# # 6. Test de la méthode get_clients_by_sales_contact
# # Scénario 1 : Aucun client trouvé
def test_get_clients_by_sales_contact_no_clients(client_controller, mock_client_dao, capsys):
    """
    Teste la récupération de clients par contact commercial lorsque aucun client n'est trouvé.
    """
    # Simuler que get_clients_by_sales_contact retourne une liste vide
    mock_client_dao.get_clients_by_sales_contact.return_value = []

    # Appeler la méthode du contrôleur
    clients = client_controller.get_clients_by_sales_contact(1)

    # Capturer les sorties standard (pour vérifier le print)
    captured = capsys.readouterr()

    # Vérifier que le message attendu est imprimé
    assert "Aucun client trouvé." in captured.out

    # Vérifier que la méthode retourne None
    assert clients is None

# Scénario 2 : Clients trouvés
def test_get_clients_by_sales_contact(client_controller, mock_client_dao, sample_client):
    """
    Teste la récupération de clients par contact commercial lorsque des clients sont trouvés.
    """
    # Simuler que get_clients_by_sales_contact retourne une liste de clients
    mock_client_dao.get_clients_by_sales_contact.return_value = [sample_client]

    # Appeler la méthode du contrôleur
    clients = client_controller.get_clients_by_sales_contact(1)

    # Vérifier que la méthode retourne les clients
    assert clients == [sample_client]


# Teste la fermeture de session
def test_close_user_controller(client_controller, mock_client_dao):
    # Appeler la méthode close
    client_controller.close()
    # Vérifier que mock_user_dao.close a été appelé
    mock_client_dao.close.assert_called_once()