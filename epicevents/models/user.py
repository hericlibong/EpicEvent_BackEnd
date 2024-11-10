from sqlalchemy import Column, Integer, String, DateTime, Enum as SqlEnum
from sqlalchemy.orm import relationship
from .base import Base
from datetime import datetime
from utils.roles import UserRole

class User(Base):
    __tablename__ ='users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=True)
    fullname = Column(String, nullable=True)
    email = Column(String, unique=True, index=True, nullable=True)
    phone = Column(String)
    department = Column(String, nullable=True)
    role = Column(SqlEnum(UserRole), nullable=False)
    date_created = Column(DateTime, default=datetime.now)
    date_updated = Column(DateTime, default=datetime.now, onupdate=datetime.now)


    # Relations
    clients = relationship('Client', back_populates='sales_contact', cascade='all, delete-orphan')
    contracts = relationship('Contract', back_populates='sales_contact', cascade='all, delete-orphan')
    events = relationship('Event', back_populates='support_contact', cascade='all, delete-orphan')