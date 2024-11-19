from dao.contract_dao import ContractDAO

class ContractController:
    def __init__(self):
        self.contract_dao = ContractDAO()

    def get_all_contracts(self):
        """
        Récupérer tous les contrats.
        """
        contracts = self.contract_dao.get_all_contracts()
        if not contracts:
            print("Aucun contrat trouvé.")
            return
        return contracts
    
    def create_contract(self, contract_data):
        """
        Créer un nouveau contrat.
        """
        try:
            contract = self.contract_dao.create_contract(contract_data)
            return contract
        except Exception as e:
            print(f"Erreur lors de la création du contrat : {e}")
            return None
        
    def get_contract_by_id(self, contract_id):
        """
        Récupérer un contrat par son identifiant.
        """
        contract = self.contract_dao.get_contract_by_id(contract_id)
        if not contract:
            print("Aucun contrat trouvé.")
            return None
        return contract
    
    def get_contracts_by_client_id(self, client_id):
        """
        Récupérer tous les contrats d'un client.
        """
        contracts = self.contract_dao.get_contracts_by_client_id(client_id)
        if not contracts:
            print("Aucun contrat trouvé.")
            return None
        return contracts
    
    def get_contract_by_sales_contact(self, sales_contact_id):
        """
        Récupérer tous les contrats d'un contact commercial.
        """
        contracts = self.contract_dao.get_contract_by_sales_contact(sales_contact_id)
        if not contracts:
            print("Aucun contrat trouvé.")
            return None
        return contracts
    
    def update_contract(self, contract_id, contract_data):
        """
        Mettre à jour un contrat.
        """
        try:
            contract = self.contract_dao.update_contract(contract_id, contract_data)
            return contract
        except Exception as e:
            print(f"Erreur lors de la mise à jour du contrat : {e}")
            return None
    
    def close(self):
        self.contract_dao.close()

   