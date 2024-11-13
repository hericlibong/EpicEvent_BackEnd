from models.event import Event
from .base_dao import BaseDAO

class EventDAO(BaseDAO):

    def create_event(self, event_data):
        """
        Créer un événement avec les données fournies.
        """
        event = Event(**event_data)
        self.session.add(event)
        self.session.commit()
        self.session.refresh(event)
        return event
    
    def get_event_by_id(self, event_id: int):
        """
        Récupère un événement par son identifiant.
        """
        return self.session.query(Event).filter_by(Event.id==event_id).first()
    
    def get_all_events(self):
        """
        Récupère tous les événements.
        """
        return self.session.query(Event).all()
    
    def update_event(self, event_id: int, event_data: dict):
        """
        Met à jour un événement avec les données fournies.
        """
        event = self.get_event_by_id(event_id)
        if not event:
            return None
        for key, value in event_data.items():
            setattr(event, key, value)
        self.session.commit()
        self.session.refresh(event)
        return event
    
    def delete_event(self, event_id: int):
        """
        Supprime un événement par son identifiant.
        """
        event = self.get_event_by_id(event_id)
        if not event:
            return False
        self.session.delete(event)
        self.session.commit()
        return True
