from models.client import Client
from .base_dao import BaseDAO
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation

class ClientDAO(BaseDAO):

    def create_client(self, client_data):
        """
        Crée un client avec les données fournies.
        """
        client = Client(**client_data)
        self.session.add(client)
        try:
            self.session.commit()

            # Recharger le client avec les relations nécessaires
            client = self.session.query(Client).options(
                joinedload(Client.sales_contact),
                # Ajoutez d'autres relations que vous souhaitez charger
            ).filter_by(id=client.id).one()

            # Détacher l'objet de la session
            self.session.expunge(client)

            # Fermer la session si nécessaire
            # self.session.close()

            return client
        
        except IntegrityError as e:
            self.session.rollback()
            # vérifier si l'erreur est une violation de contrainte unique
            if isinstance(e.orig, UniqueViolation):
                # Extraire le nom de la contrainte unique
                constraint_name = e.orig.diag.constraint_name
                if constraint_name == 'ix_clients_email':
                    raise ValueError("Adresse email déjà utilisée.") from e
                # elif constraint_name == 'ix_client_phone':
                #     raise ValueError("Numéro de téléphone déjà utilisé.") from e
                else:
                    raise ValueError("Erreur de contrainte unique non gérée.") from e
            else:
                # Remonter l'exception pour les autres erreurs d'intégrité
                raise Exception("Erreur d'intégrité non gérée.") from e

   
       
    
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
