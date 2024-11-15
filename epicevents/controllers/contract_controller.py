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
    
    def close(self):
        self.contract_dao.close()