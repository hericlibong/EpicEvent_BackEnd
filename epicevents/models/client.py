from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base
from datetime import datetime


class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, nullable=False)
    company_name = Column(String, nullable=False)
    date_created = Column(DateTime, default=datetime.now)
    date_updated = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    sales_contact_id = Column(Integer, ForeignKey('users.id'))

    # Relations
    sales_contact = relationship('User', back_populates='clients')
    contracts = relationship('Contract', back_populates='client', cascade='all, delete-orphan')
