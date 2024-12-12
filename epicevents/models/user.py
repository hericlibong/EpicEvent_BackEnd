from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base
from datetime import datetime


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    fullname = Column(String, nullable=True)
    email = Column(String, unique=True, index=True, nullable=True)
    phone = Column(String, nullable=True)
    department_id = Column(Integer, ForeignKey('departments.id'), nullable=False)
    date_created = Column(DateTime, default=datetime.now)
    date_updated = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Relations
    clients = relationship('Client', back_populates='sales_contact', cascade='all, delete-orphan')
    contracts = relationship('Contract', back_populates='sales_contact', cascade='all, delete-orphan')
    events = relationship('Event', back_populates='support_contact', cascade='all, delete-orphan')
    department = relationship('Department', back_populates='users')

    def __repr__(self):
        return f'<User: {self.username}, department: {self.department.name}>'
