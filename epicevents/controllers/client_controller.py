# controllers/client_controller.py
from dao.client_dao import ClientDAO
from utils.log_decorator import log_exceptions
from utils.logger import get_logger


class ClientController:
    def __init__(self):
        self.client_dao = ClientDAO()
        self.logger = get_logger('controller')

    @log_exceptions('controller')
    def get_all_clients(self):
        """
        Récupérer tous les clients.
        """
        clients = self.client_dao.get_all_clients()
        if not clients:
            print("Aucun client trouvé.")
            return
        return clients
    
    #@log_exceptions('controller')
    def create_client(self, client_data):
        """
        Créer un nouveau client.
        """
        # Validation des données
        if not client_data.get('fullname'):
            raise ValueError("Le nom complet est obligatoire.")
        if not client_data.get('email'):
            raise ValueError("L'adresse email est obligatoire.")
        if not client_data.get('phone'):
            raise ValueError("Le numéro de téléphone est obligatoire.")
        if not client_data.get('company_name'):
            raise ValueError("Le nom de l'entreprise est obligatoire.")
        
        client = self.client_dao.create_client(client_data)       
        return client
        
            
    @log_exceptions('controller')
    def get_client_by_id(self, client_id):
        """
        Récupérer un client par son identifiant.
        """
        client = self.client_dao.get_client_by_id(client_id)
        if not client:
            print("Aucun client trouvé.")
            return None
        return client
    
    @log_exceptions('controller')
    def update_client(self, client_id, client_data):
        """
        Mettre à jour un client.
        """
        client = self.client_dao.update_client(client_id, client_data)
        if not client:
            print("Aucun client trouvé ou erreur lors de la mise à jour.")
            return None
        return client
              
    @log_exceptions('controller')
    def get_clients_by_sales_contact(self, sales_contact_id):     
        """
        Récupérer tous les clients d'un contact commercial.
        """
        clients = self.client_dao.get_clients_by_sales_contact(sales_contact_id)
        if not clients:
            print("Aucun client trouvé.")
            return None
        return clients
    
    @log_exceptions('controller')
    def delete_client(self, client_id):
        """
        Supprimer un client par son identifiant.
        """
        result = self.client_dao.delete_client(client_id)
        return result
    
    @log_exceptions('controller')
    def close(self):
        self.client_dao.close()

    
    