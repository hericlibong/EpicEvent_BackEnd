from models.client import Client
from .base_dao import BaseDAO

class ClientDAO(BaseDAO):

    def create_client(self, client_data):
        """
        Créer un client avec les données fournies.
        """
        client = Client(**client_data)
        self.session.add(client)
        self.session.commit()
        self.session.refresh(client)
        return client
    
    def get_client_by_id(self, client_id: int):
        """
        Récupère un client par son identifiant.
        """
        return self.session.query(Client).filter_by(id=client_id).first()
    
    def get_all_clients(self):
        """
        Récupère tous les clients.
        """
        return self.session.query(Client).all()
    
    def update_client(self, client_id: int, client_data: dict):
        """
        Met à jour un client avec les données fournies.
        """
        client = self.get_client_by_id(client_id)
        if not client:
            return None
        for key, value in client_data.items():
            setattr(client, key, value)
        self.session.commit()
        self.session.refresh(client)
        return client
    
    def get_clients_by_sales_contact(self, sales_contact_id: int):
        """
        Récupère tous les clients d'un contact commercial.
        """
        return self.session.query(Client).filter_by(sales_contact_id=sales_contact_id).all()
    
    def delete_client(self, client_id: int):
        """
        Supprime un client par son identifiant.
        """
        client = self.get_client_by_id(client_id)
        if not client:
            return False
        self.session.delete(client)
        self.session.commit()
        return True
