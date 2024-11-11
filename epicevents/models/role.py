from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base

class Role(Base):
    """
    Role model representing a user role in the system.
    Attributes:
        id (int): Unique identifier for the role.
        name (str): Name of the role, must be unique and not null.
        description (str): Description of the role, cannot be null.
        users (relationship): Relationship to the User model, indicating users assigned to this role.
    """
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=False)

    # Relations
    users = relationship('User', back_populates='role')