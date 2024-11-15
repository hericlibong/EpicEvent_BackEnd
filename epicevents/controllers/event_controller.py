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
            return
        return events
    
    def close(self):
        self.event_dao.close()