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
    
    def create_client(self, client_data):
        """
        Créer un nouveau client.
        """
        try:
            client = self.client_dao.create_client(client_data)
            return client
        except Exception as e:
            print(f"Erreur lors de la création du client : {e}")
            return None
    
    def get_client_by_id(self, client_id):
        """
        Récupérer un client par son identifiant.
        """
        client = self.client_dao.get_client_by_id(client_id)
        if not client:
            print("Aucun client trouvé.")
            return None
        return client
    
    def update_client(self, client_id, client_data):
        """
        Mettre à jour un client.
        """
        try:
            client = self.client_dao.update_client(client_id, client_data)
            if not client:
                print("Aucun client trouvé ou erreur lors de la mise à jour.")
                return None
            return client
        except Exception as e:
            print(f"Erreur lors de la mise à jour du client : {e}")
            return None
    
    def get_clients_by_sales_contact(self, sales_contact_id):     
        """
        Récupérer tous les clients d'un contact commercial.
        """
        clients = self.client_dao.get_clients_by_sales_contact(sales_contact_id)
        if not clients:
            print("Aucun client trouvé.")
            return None
        return clients
    
    def close(self):
        self.client_dao.close()