from dao.event_dao import EventDAO
from dao.contract_dao import ContractDAO
from dao.user_dao import UserDAO
from datetime import datetime, timedelta
from utils.logger import get_logger, log_error

logger = get_logger('events')


class EventController:
    def __init__(self):
        self.event_dao = EventDAO()
        self.contract_dao = ContractDAO()
        self.user_dao = UserDAO()

    def parse_datetime(self, date_str):
        # Supposons le format JJ/MM/AAAA HH:MM
        return datetime.strptime(date_str, "%d/%m/%Y")

    def validate_event_dates(self, start_dt, end_dt):
        now = datetime.now()
        # L'événement doit commencer au plus tôt demain (now + 1 jour)
        if start_dt < (now + timedelta(days=1)):
            raise ValueError("La date de début doit être au moins demain.")
        if end_dt <= start_dt:
            raise ValueError("La date de fin doit être postérieure à la date de début.")

    def create_event(self, event_data, user_id):
        # Récupérer le contrat
        contract_id = event_data.get('contract_id')
        if not contract_id:
            raise ValueError("L'ID du contrat est obligatoire.")

        contract = self.contract_dao.get_contract_by_id(contract_id)
        if not contract:
            raise ValueError("Contrat introuvable.")
        # Contrat doit être signé
        if not contract.status:
            raise ValueError("Le contrat n'est pas signé, impossible de créer un événement.")
        # Vérifier que le commercial du contrat correspond à l'utilisateur
        if contract.sales_contact_id != user_id:
            raise ValueError("Vous n'êtes pas le commercial responsable de ce contrat.")
        # Vérifier si un évènement existe déjà pour ce contrat
        existing_event = self.event_dao.get_event_by_contract_id(contract_id)
        if existing_event:
            raise ValueError("Un événement est déjà associé à ce contrat.")

        # Valider les dates
        start_str = event_data.get('event_date_start_str')
        end_str = event_data.get('event_date_end_str')
        start_dt = self.parse_datetime(start_str)
        end_dt = self.parse_datetime(end_str)
        self.validate_event_dates(start_dt, end_dt)

        # Créer l'événement
        try:
            event = self.event_dao.create_event({
                'name': event_data.get('name', ''),
                'contract_id': contract_id,
                'event_date_start': start_dt,
                'event_date_end': end_dt,
                'location': event_data.get('location', ''),
                'attendees': event_data.get('attendees', 0),
                'notes': event_data.get('notes', ''),
                # support_contact_id sera assigné ultérieurement
            })
            return event
        except ValueError as ve:
            raise ve
        except Exception as e:
            log_error(logger, "Erreur inattendue lors de la création de l'événement", exception=e)
            raise Exception("Erreur lors de la création de l'événement") from e
        finally:
            self.event_dao.close()
            self.contract_dao.close()

    def get_event_by_id(self, event_id):
        event = self.event_dao.get_event_by_id(event_id)
        self.event_dao.close()
        self.contract_dao.close()
        return event

    def update_event(self, event_id, event_data):
        try:
            event = self.event_dao.get_event_by_id(event_id)
            if not event:
                raise ValueError("Evènement introuvable.")

            # Vérifier si l'événement est déjà passé
            now = datetime.now()
            if event.event_date_end < now:
                raise ValueError("L'évènement est déjà passé, impossible de le modifier.")

            # Vérifier les nouvelles dates si fournies
            start_str = event_data.get('event_date_start_str', event.event_date_start.strftime("%d/%m/%Y %H:%M"))
            end_str = event_data.get('event_date_end_str', event.event_date_end.strftime("%d/%m/%Y %H:%M"))
            start_dt = self.parse_datetime(start_str)
            end_dt = self.parse_datetime(end_str)
            self.validate_event_dates(start_dt, end_dt)

            updated_event = self.event_dao.update_event(event_id, {
                'name': event_data.get('name', event.name),
                'support_contact_id': event_data.get('support_contact_id', event.support_contact_id),
                'event_date_start': start_dt,
                'event_date_end': end_dt,
                'location': event_data.get('location', event.location),
                'attendees': event_data.get('attendees', event.attendees),
                'notes': event_data.get('notes', event.notes),
            })
            return updated_event

        except ValueError as ve:
            raise ve
        except Exception as e:
            log_error(logger, "Erreur inattendue lors de la mise à jour de l'événement", exception=e)
            raise Exception("Erreur lors de la mise à jour de l'événement") from e
        finally:
            self.event_dao.close()
            self.contract_dao.close()

    def get_all_events(self):
        """
        Récupérer tous les événements.
        """
        events = self.event_dao.get_all_events()
        if not events:
            print("Aucun événement trouvé.")
            return []
        return events

    def assign_support(self, event_id, support_user_id):
        """
        Assigner un contact de support à un événement.
        """
        # Récupérer l'utilisateur à assigner
        support_user = self.user_dao.get_user_by_id(support_user_id)
        if support_user is None:
            raise ValueError("Utilisateur de support introuvable.")

        # Vérifier que l'utilisateur appartient au département de support
        if support_user.department.lower() != 'support':
            raise ValueError("Utilisateur n'appartient pas au département de support.")

        # Si l'utilisateur est bien du support, assigner le support à l'événement
        event = self.event_dao.assign_support(event_id, support_user_id)
        if not event:
            raise ValueError("Aucun événement trouvé.")

        return event

    def get_events_by_support(self, support_user_id):
        """
        Récupérer tous les événements d'un contact de support.
        """
        events = self.event_dao.get_events_by_support(support_user_id)
        if not events:
            print("Aucun événement trouvé.")
            return []
        return events

    def close(self):
        self.event_dao.close()
        self.contract_dao.close()
