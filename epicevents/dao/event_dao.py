# from models.event import Event
# from .base_dao import BaseDAO
# from sqlalchemy.orm import joinedload
# from models.contract import Contract

# class EventDAO(BaseDAO):

#     def create_event(self, event_data):
#         """
#         Créer un événement avec les données fournies.
#         """
#         event = Event(**event_data)
#         self.session.add(event)
#         self.session.commit()
#         self.session.refresh(event)
#         return event
    
#     def get_event_by_id(self, event_id: int):
#         """
#         Récupère un événement par son identifiant.
#         """
#         return self.session.query(Event).filter_by(id=event_id).first()
    
    
#     def get_all_events(self):
#         """
#         Récupère tous les événements.
#         """
#         return self.session.query(Event).options(
#             joinedload(Event.contract).joinedload(Contract.client),
#             joinedload(Event.support_contact)
#         ).all()
    
#     def update_event(self, event_id: int, event_data: dict):
#         """
#         Met à jour un événement avec les données fournies.
#         """
#         event = self.get_event_by_id(event_id)
#         if not event:
#             return None
#         for key, value in event_data.items():
#             setattr(event, key, value)
#         self.session.commit()
#         self.session.refresh(event)
#         return event
    
#     def assign_support(self, event_id, support_user_id):
#         event = self.get_event_by_id(event_id)
#         if event:
#             event.support_contact_id = support_user_id
#             self.session.commit()
#             self.session.refresh(event)
#             return event
#         return None

#     def get_events_by_support(self, support_user_id):
#         return self.session.query(Event).options(
#             joinedload(Event.contract).joinedload(Contract.client),
#             joinedload(Event.support_contact)
#         ).filter_by(support_contact_id=support_user_id).all()
    
#     def delete_event(self, event_id: int):
#         """
#         Supprime un événement par son identifiant.
#         """
#         event = self.get_event_by_id(event_id)
#         if not event:
#             return False
#         self.session.delete(event)
#         self.session.commit()
#         return True

from models.event import Event
from .base_dao import BaseDAO
from sqlalchemy.orm import joinedload
from models.contract import Contract
from utils.logger import get_logger, log_error
from sqlalchemy.exc import SQLAlchemyError

logger = get_logger('events')

class EventDAO(BaseDAO):

    def create_event(self, event_data):
        """
        Créer un événement avec les données fournies.
        """
        event = Event(**event_data)
        self.session.add(event)
        try:
            self.session.commit()
            self.session.refresh(event)
            return event
        except SQLAlchemyError as e:
            self.session.rollback()
            log_error(logger, "Erreur inattendue lors de la création de l'événement", exception=e)
            raise Exception("Erreur lors de la création de l'événement") from e

    def get_event_by_id(self, event_id: int):
        """
        Récupère un événement par son identifiant.
        """
        try:
            return self.session.query(Event).filter_by(id=event_id).first()
        except SQLAlchemyError as e:
            log_error(logger, "Erreur inattendue lors de la récupération de l'événement par ID", exception=e)
            raise Exception("Erreur lors de la récupération de l'événement") from e

    def get_event_by_contract_id(self, contract_id: int):
        """
        Récupère un événement par l'identifiant du contrat.
        """
        try:
            return self.session.query(Event).filter_by(contract_id=contract_id).first()
        except SQLAlchemyError as e:
            log_error(logger, "Erreur inattendue lors de la récupération de l'événement par contrat", exception=e)
            raise Exception("Erreur lors de la récupération de l'événement par contrat") from e

    def get_all_events(self):
        """
        Récupère tous les événements.
        """
        try:
            return self.session.query(Event).options(
                joinedload(Event.contract).joinedload(Contract.client),
                joinedload(Event.support_contact)
            ).all()
        except SQLAlchemyError as e:
            log_error(logger, "Erreur inattendue lors de la récupération de tous les événements", exception=e)
            raise Exception("Erreur lors de la récupération des événements") from e

    def update_event(self, event_id: int, event_data: dict):
        """
        Met à jour un événement avec les données fournies.
        """
        try:
            event = self.get_event_by_id(event_id)
            if not event:
                return None
            for key, value in event_data.items():
                setattr(event, key, value)
            self.session.commit()
            self.session.refresh(event)
            return event
        except SQLAlchemyError as e:
            self.session.rollback()
            log_error(logger, "Erreur inattendue lors de la mise à jour de l'événement", exception=e)
            raise Exception("Erreur lors de la mise à jour de l'événement") from e

    def assign_support(self, event_id, support_user_id):
        try:
            event = self.get_event_by_id(event_id)
            if not event:
                return None
            event.support_contact_id = support_user_id
            self.session.commit()
            self.session.refresh(event)
            return event
        except SQLAlchemyError as e:
            self.session.rollback()
            log_error(logger, "Erreur inattendue lors de l'assignation du support à l'événement", exception=e)
            raise Exception("Erreur lors de l'assignation du support") from e

    def get_events_by_support(self, support_user_id):
        try:
            return self.session.query(Event).options(
                joinedload(Event.contract).joinedload(Contract.client),
                joinedload(Event.support_contact)
            ).filter_by(support_contact_id=support_user_id).all()
        except SQLAlchemyError as e:
            log_error(logger, "Erreur inattendue lors de la récupération des événements par support", exception=e)
            raise Exception("Erreur lors de la récupération des événements par support") from e

    def delete_event(self, event_id: int):
        """
        Supprime un événement par son identifiant.
        """
        try:
            event = self.get_event_by_id(event_id)
            if not event:
                return False
            self.session.delete(event)
            self.session.commit()
            return True
        except SQLAlchemyError as e:
            self.session.rollback()
            log_error(logger, "Erreur inattendue lors de la suppression de l'événement", exception=e)
            raise Exception("Erreur lors de la suppression de l'événement") from e
