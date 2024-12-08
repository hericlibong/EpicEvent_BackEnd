# controllers/client_controller.py
from dao.client_dao import ClientDAO
from sentry_sdk import capture_exception, capture_message

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
        # Validation des données
        if not client_data.get('fullname'):
            raise ValueError("Le nom complet est obligatoire.")
        if not client_data.get('email'):
            raise ValueError("L'adresse email est obligatoire.")
        if not client_data.get('phone'):
            raise ValueError("Le numéro de téléphone est obligatoire.")
        if not client_data.get('company_name'):
            raise ValueError("Le nom de l'entreprise est obligatoire.")
        
        try:
            client = self.client_dao.create_client(client_data)

            # Journaliser le succès
            # capture_message(
            #     f"Client créé avec succès : {client.fullname} (ID : {client.id})",
            #     level="info")
            return client
        
        except ValueError as e:
            # Transmettre l'erreur à la couche supérieure
            # Journaliser une erreur métier
            capture_message(f"Erreur métier : {e}", level="warning")
            raise e
        
        except Exception as e:
            # Journaliser une erreur inattendue
            capture_exception(e)
            raise Exception("Erreur lors de la création du client") from e
        finally:
            # Fermer la session pour libérer les ressources
            self.client_dao.close()
            
    
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

    
    def delete_client(self, client_id):
        """
        Supprimer un client par son identifiant.
        """
        result = self.client_dao.delete_client(client_id)
        return result