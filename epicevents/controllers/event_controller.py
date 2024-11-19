from dao.event_dao import EventDAO

class EventController:
    def __init__(self):
        self.event_dao = EventDAO()
    
    def get_all_events(self):
        """
        Récupérer tous les événements.
        """
        events = self.event_dao.get_all_events()
        if not events:
            print("Aucun événement trouvé.")
            return []
        return events

    def create_event(self, event_data):
        """
        Créer un nouvel événement.
        """
        try:
            event = self.event_dao.create_event(event_data)
            return event
        except Exception as e:
            print(f"Erreur lors de la création de l'événement : {e}")
            return None
        
    def get_event_by_id(self, event_id):
        """
        Récupérer un événement par son identifiant.
        """
        event = self.event_dao.get_event_by_id(event_id)
        if not event:
            print("Aucun événement trouvé.")
            return None
        return event
    
    def update_event(self, event_id, event_data):
        """
        Mettre à jour un événement.
        """
        try:
            event = self.event_dao.update_event(event_id, event_data)
            if not event:
                print("Aucun événement trouvé ou erreur lors de la mise à jour.")
                return None
            return event
        except Exception as e:
            print(f"Erreur lors de la mise à jour de l'événement : {e}")
            return None
        
    def assign_support(self, event_id, support_user_id):
        """
        Assigner un contact de support à un événement.
        """
        event = self.event_dao.assign_support(event_id, support_user_id)
        if not event:
            print("Aucun événement trouvé.")
            return None
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