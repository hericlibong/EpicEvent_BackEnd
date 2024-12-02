import pytest
from unittest.mock import MagicMock
from controllers.contract_controller import ContractController
from models.contract import Contract

@pytest.fixture
def mock_contract_dao():
    dao = MagicMock()
    return dao

@pytest.fixture
def contract_controller(mock_contract_dao):
    controller = ContractController()
    controller.contract_dao = mock_contract_dao
    return controller

@pytest.fixture
def sample_contract():
    """
    Simule un contrat pour les tests.
    """
    return Contract(
        id=1,
        client_id=1,
        sales_contact_id=1,
        status=True,
        amount=10000.0,
        remaining_amount=5000.0
    )


# Teste aucun contrat trouvé
def test_get_all_contracts_no_contracts(contract_controller, mock_contract_dao, capsys):
    """
    Teste la récupération de contrats lorsque aucun contrat n'est trouvé.
    """
    # Simuler que get_all_contracts retourne une liste vide
    mock_contract_dao.get_all_contracts.return_value = []

    # Appeler la méthode du contrôleur
    contracts = contract_controller.get_all_contracts()

    # Capturer les sorties standard (pour vérifier le print)
    captured = capsys.readouterr()

    # Vérifier que le message attendu est imprimé
    assert "Aucun contrat trouvé." in captured.out

    # Vérifier que la méthode retourne None
    assert contracts is None

# Teste la récupération de contrats
def test_get_all_contracts(contract_controller, mock_contract_dao, sample_contract):
    """
    Teste la récupération de tous les contrats.
    """
    # Simuler que get_all_contracts retourne une liste de contrats
    mock_contract_dao.get_all_contracts.return_value = [sample_contract]

    # Appeler la méthode du contrôleur
    contracts = contract_controller.get_all_contracts()

    # Vérifier que la méthode retourne les contrats
    assert contracts == [sample_contract]

# Teste la création d'un contrat avec des données valides
def test_create_contract_with_valid_data(contract_controller, mock_contract_dao, sample_contract):
    """
    Teste la création d'un contrat avec des données valides.
    """
    # Simuler que create_contract retourne un contrat
    mock_contract_dao.create_contract.return_value = sample_contract

    # Données de contrat valides
    contract_data = {
        "client_id": 1,
        "sales_contact_id": 1,
        "status": True,
        "amount": 10000.0,
        "remaining_amount": 5000.0,
    }

    # Appeler la méthode du contrôleur avec des données valides
    contract = contract_controller.create_contract(contract_data)

    # Vérifier que la méthode retourne le contrat attendu
    assert contract == sample_contract

    # Vérifier que la méthode du DAO a été appelée avec les bonnes données
    mock_contract_dao.create_contract.assert_called_once_with(contract_data)

# Teste échec de la création d'un contrat
def test_create_contract_failure(contract_controller, mock_contract_dao, capsys):
    """
    Teste l'échec de la création d'un contrat.
    """
    # Simuler une exception lors de la création du contrat
    mock_contract_dao.create_contract.side_effect = Exception("Erreur lors de la création du contrat")

    # Appeler la méthode du contrôleur avec des données simulées
    contract_data = {"client_id": 1, "sales_contact_id": 1, "amount": 1000.0, "remaining_amount": 500.0}
    created_contract = contract_controller.create_contract(contract_data)

    # Capturer les messages imprimés
    captured = capsys.readouterr()

    # Vérifier que la méthode retourne None
    assert created_contract is None

    # Vérifier que le message d'erreur attendu est imprimé
    assert "Erreur lors de la création du contrat" in captured.out

### **Tests pour `get_contract_by_id`**

# 1. **Scénario 1 : Contrat introuvable**
def test_get_contract_by_id_not_found(contract_controller, mock_contract_dao, capsys):
    """
    Teste la récupération d'un contrat par ID lorsque le contrat n'est pas trouvé.
    """
    # Simuler que get_contract_by_id retourne None
    mock_contract_dao.get_contract_by_id.return_value = None

    # Appeler la méthode du contrôleur
    contract = contract_controller.get_contract_by_id(1)

    # Capturer les sorties standard (pour vérifier le print)
    captured = capsys.readouterr()

    # Vérifier que le message attendu est imprimé
    assert "Aucun contrat trouvé." in captured.out

    # Vérifier que la méthode retourne None
    assert contract is None

# 2. **Scénario 2 : Contrat trouvé**
def test_get_contract_by_id_found(contract_controller, mock_contract_dao, sample_contract):
    """
    Teste la récupération d'un contrat par ID lorsque le contrat est trouvé.
    """
    # Simuler que get_contract_by_id retourne un contrat
    mock_contract_dao.get_contract_by_id.return_value = sample_contract

    # Appeler la méthode du contrôleur
    contract = contract_controller.get_contract_by_id(1)

    # Vérifier que la méthode retourne le contrat simulé
    assert contract == sample_contract


### **Tests pour `get_contract_by_sales_contact`**

# 1. **Scénario 1 : Aucun contrat trouvé**
def test_get_contract_by_sales_contact_no_contracts(contract_controller, mock_contract_dao, capsys):
    """
    Teste la récupération de contrats par contact commercial lorsque aucun contrat n'est trouvé.
    """
    # Simuler que get_contract_by_sales_contact retourne une liste vide
    mock_contract_dao.get_contract_by_sales_contact.return_value = []

    # Appeler la méthode du contrôleur
    contracts = contract_controller.get_contract_by_sales_contact(1)

    # Capturer les sorties standard (pour vérifier le print)
    captured = capsys.readouterr()

    # Vérifier que le message attendu est imprimé
    assert "Aucun contrat trouvé." in captured.out

    # Vérifier que la méthode retourne None
    assert contracts is None

# 2. **Scénario 2 : Contrats trouvés**
def test_get_contract_by_sales_contact_found(contract_controller, mock_contract_dao, sample_contract):
    """
    Teste la récupération de contrats par contact commercial lorsque des contrats sont trouvés.
    """
    # Simuler que get_contract_by_sales_contact retourne une liste de contrats
    mock_contract_dao.get_contract_by_sales_contact.return_value = [sample_contract]

    # Appeler la méthode du contrôleur
    contracts = contract_controller.get_contract_by_sales_contact(1)

    # Vérifier que la méthode retourne les contrats simulés
    assert contracts == [sample_contract]

### **Tests pour `get_contracts_by_client_id`**

# 1. **Scénario 1 : Aucun contrat trouvé**
def test_get_contracts_by_client_id_no_contracts(contract_controller, mock_contract_dao, capsys):
    """
    Teste la récupération de contrats par client lorsque aucun contrat n'est trouvé.
    """
    # Simuler que get_contracts_by_client_id retourne une liste vide
    mock_contract_dao.get_contracts_by_client_id.return_value = []

    # Appeler la méthode du contrôleur
    contracts = contract_controller.get_contracts_by_client_id(1)

    # Capturer les sorties standard (pour vérifier le print)
    captured = capsys.readouterr()

    # Vérifier que le message attendu est imprimé
    assert "Aucun contrat trouvé." in captured.out

    # Vérifier que la méthode retourne None
    assert contracts is None

# 2. **Scénario 2 : Contrats trouvés**
def test_get_contracts_by_client_id_found(contract_controller, mock_contract_dao, sample_contract):
    """
    Teste la récupération de contrats par client lorsque des contrats sont trouvés.
    """
    # Simuler que get_contracts_by_client_id retourne une liste de contrats
    mock_contract_dao.get_contracts_by_client_id.return_value = [sample_contract]

    # Appeler la méthode du contrôleur
    contracts = contract_controller.get_contracts_by_client_id(1)

    # Vérifier que la méthode retourne les contrats simulés
    assert contracts == [sample_contract]

### **Tests pour `update_contract`**
# 1. **Scénario 1 : Mise à jour réussie**
def test_update_contract_success(contract_controller, mock_contract_dao, sample_contract):
    """
    Teste la mise à jour d'un contrat avec succès.
    """
    # Simuler que update_contract retourne un contrat mis à jour
    updated_contract = sample_contract
    updated_contract.amount = 15000.0
    mock_contract_dao.update_contract.return_value = updated_contract

    # Données de mise à jour du contrat
    update_data = {
        "amount": 15000.0,
        "remaining_amount": 7000.0,
    }

    # Appeler la méthode du contrôleur
    contract = contract_controller.update_contract(1, update_data)

    # Vérifier que la méthode retourne le contrat mis à jour
    assert contract == updated_contract

    # Vérifier que la méthode du DAO a été appelée avec les bonnes données
    mock_contract_dao.update_contract.assert_called_once_with(1, update_data)

# 2. **Scénario 2 : Erreur lors de la mise à jour**
def test_update_contract_failure(contract_controller, mock_contract_dao, capsys):
    """
    Teste l'échec de la mise à jour d'un contrat.
    """
    # Simuler une exception lors de la mise à jour du contrat
    mock_contract_dao.update_contract.side_effect = Exception("Erreur lors de la mise à jour du contrat")

    # Données de mise à jour du contrat
    update_data = {
        "amount": 15000.0,
        "remaining_amount": 7000.0,
    }

    # Appeler la méthode du contrôleur
    contract = contract_controller.update_contract(1, update_data)

    # Capturer les messages imprimés
    captured = capsys.readouterr()

    # Vérifier que la méthode retourne None
    assert contract is None

    # Vérifier que le message d'erreur attendu est imprimé
    assert "Erreur lors de la mise à jour du contrat" in captured.out

# Teste la fermeture de session
def test_close_user_controller(contract_controller, mock_contract_dao):
    # Appeler la méthode close
    contract_controller.close()
    # Vérifier que mock_user_dao.close a été appelé
    mock_contract_dao.close.assert_called_once()



  

