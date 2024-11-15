# controllers/client_controller.py
from dao.client_dao import ClientDAO

class ClientController:
    def __init__(self):
        self.client_dao = ClientDAO()

    def get_all_clients(self):
        """
        Récupérer tous les clients.
        """
        clients = self.client_dao.get_all_clients()
        if not clients:
            print("Aucun client trouvé.")
            return
        return clients
    
    def close(self):
        self.client_dao.close()