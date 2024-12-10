from dao.contract_dao import ContractDAO
from dao.client_dao import ClientDAO
from utils.logger import get_logger, log_info, log_error
from utils.log_decorator import log_exceptions

logger = get_logger('contracts')

class ContractController:
    def __init__(self):
        self.contract_dao = ContractDAO()
        self.client_dao = ClientDAO()
        self.logger = logger
    

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
        client_id = contract_data.get('client_id')
        if not client_id:
            raise ValueError("L'ID du client est obligatoire pour créer un contrat.")

        client = self.client_dao.get_client_by_id(client_id)
        if not client:
            raise ValueError("Client introuvable.")

        # On assigne directement le commercial du client au contrat
        contract_data['sales_contact_id'] = client.sales_contact_id

         # Vérification si le contrat est signé dès la création
        if contract_data.get('status') == True:
            # Vérifier qu'il est entièrement payé
            if contract_data.get('remaining_amount', 0) > 0:
                raise ValueError("Le contrat doit être entièrement payé avant d'être signé.")

        try:
            contract = self.contract_dao.create_contract(contract_data)
            return contract
        except ValueError as e:
            # Erreur métier (ex: email déjà utilisée dans le DAO)
            raise e
        except Exception as e:
            # Erreur inattendue
            log_error(self.logger, "Erreur inattendue lors de la création du contrat", exception=e)
            raise Exception("Erreur lors de la création du contrat") from e
        finally:
            self.contract_dao.close()
            self.client_dao.close()
        
        
    def get_contract_by_id(self, contract_id):
        """
        Récupérer un contrat par son identifiant.
        """
        contract = self.contract_dao.get_contract_by_id(contract_id)
        self.contract_dao.close()
        self.client_dao.close()
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
            # Récupérer le contrat initial pour vérifier s'il existe
            contract = self.contract_dao.get_contract_by_id(contract_id)
            if not contract:
                # Erreur métier : contrat introuvable
                raise ValueError("Contrat introuvable.")
            
            # Si le contrat est déjà signé, aucune modification possible
            if contract.status == True:
                raise ValueError("Contrat déjà signé, modification impossible.")

            # Vérifier si on tente de signer le contrat (status: False -> True)
            new_status = contract_data.get('status', contract.status)
            if contract.status == False and new_status == True:
                # On tente de signer, vérifier que remaining_amount == 0
                if contract_data.get('remaining_amount', contract.remaining_amount) > 0:
                    raise ValueError("Le contrat doit être entièrement payé avant d'être signé.")

            # Mise à jour du contrat
            updated_contract = self.contract_dao.update_contract(contract_id, contract_data)
            return updated_contract
        
        except ValueError as ve:
            # Erreur métier connue (par ex. si DAO renvoie None => Contrat non trouvé)
            raise ve
        except Exception as e:
            log_error(self.logger, "Erreur inattendue lors de la mise à jour du contrat", exception=e)
            raise Exception("Erreur lors de la mise à jour du contrat") from e
        finally:
            self.contract_dao.close()
            self.client_dao.close()

    def delete_contract(self, contract_id):
        """
        Supprimer un contrat par son identifiant.
        """
        try:
            contract = self.contract_dao.get_contract_by_id(contract_id)
            if not contract:
                raise ValueError("Contrat introuvable.")
            
            # Si le contrat est signé, pas de suppression
            if contract.status == True:
                raise ValueError("Contrat déjà signé, suppression impossible.")
            
            # Interdire la suppression si entièrement payé et non signé:
            # if contract.remaining_amount == 0 and contract.status == False:
            #     raise ValueError("Contrat entièrement payé, il devrait être signé, suppression impossible.")
            
            # Supprimer le contrat via le DAO
            result = self.contract_dao.delete_contract(contract_id)

            if not result:
                # Si le DAO retourne False quand le contrat n'existe pas
                # On peut considérer cela comme une erreur métier
                raise ValueError("Contrat introuvable ou déjà supprimé.")
            
            # Si result est True, tout va bien, pas besoin de log ici,
            # la vue s'en charge.
            return True

        except ValueError as ve:
            # Erreur métier (contrat introuvable), on la relance sans log_error
            raise ve
        except Exception as e:
            # Erreur inattendue
            log_error(self.logger, "Erreur inattendue lors de la suppression du contrat", exception=e)
            raise Exception("Erreur lors de la suppression du contrat") from e
        finally:
            self.contract_dao.close()
            self.client_dao.close()  # Supposant l’existence d’un client_dao


    
    def close(self):
        self.contract_dao.close()

   