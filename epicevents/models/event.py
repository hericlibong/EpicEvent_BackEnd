from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base
from datetime import datetime

class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True, index=True)
    contract_id = Column(Integer, ForeignKey('contracts.id'), nullable=False)
    support_contact_id = Column(Integer, ForeignKey('users.id'))
    event_date_start = Column(DateTime, nullable=False)
    event_date_end = Column(DateTime, nullable=False)
    location = Column(String, nullable=False)
    attendees = Column(Integer)
    notes = Column(Text)
    date_created = Column(DateTime, default=datetime.now)
    date_updated = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Relations
    contract = relationship('Contract', back_populates='events')
    support_contact = relationship('User', back_populates='events')


    