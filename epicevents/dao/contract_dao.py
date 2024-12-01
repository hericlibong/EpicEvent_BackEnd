from models.contract import Contract
from .base_dao import BaseDAO
from sqlalchemy.orm import joinedload

class ContractDAO(BaseDAO):

    def create_contract(self, contract_data):
        """
        Créer un contrat avec les données fournies.
        """
        contract = Contract(**contract_data)
        self.session.add(contract)

        self.session.commit()
        contract = self.session.query(Contract).options(
            joinedload(Contract.client), 
            joinedload(Contract.sales_contact)).filter_by(id=contract.id).one()
        self.session.expunge(contract)
        # self.session.refresh(contract)
        return contract
    
    def get_contract_by_id(self, contract_id: int):
        """
        Récupère un contrat par son identifiant.
        """
        return self.session.query(Contract).filter_by(id=contract_id).first()
    
    
    def get_all_contracts(self):
        """
        Récupère tous les contrats.
        """
        return self.session.query(Contract).options(
            joinedload(Contract.client), 
            joinedload(Contract.sales_contact)).all()
    
    def update_contract(self, contract_id: int, contract_data: dict):
        """
        Met à jour un contrat avec les données fournies.
        """
        contract = self.get_contract_by_id(contract_id)
        if not contract:
            return None
        for key, value in contract_data.items():
            setattr(contract, key, value)
        self.session.commit()
        self.session.refresh(contract)
        return contract
    
    def get_contracts_by_client_id(self, client_id: int):
        """
        Récupère tous les contrats d'un client.
        """
        return self.session.query(Contract).filter_by(client_id=client_id).all()
    
    def get_contract_by_sales_contact(self, sales_contact_id: int):
        """
        Récupère tous les contrats d'un contact commercial.
        """
        return self.session.query(Contract).options(
            joinedload(Contract.client), 
            joinedload(Contract.sales_contact)).filter_by(sales_contact_id=sales_contact_id).all()
        
    
    def delete_contract(self, contract_id: int):
        """
        Supprime un contrat par son identifiant.
        """
        contract = self.get_contract_by_id(contract_id)
        if not contract:
            return False
        self.session.delete(contract)
        self.session.commit()
        return True
