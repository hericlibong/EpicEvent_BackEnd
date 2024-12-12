from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base


class Department(Base):
    """
    Department model representing a department within an organization.
    Attributes:
        id (int): Unique identifier for the department.
        name (str): Name of the department, must be unique and not null.
        description (str): Description of the department, cannot be null.
        users (relationship): Relationship to the User model, representing users belonging to this department.
    """
    __tablename__ = 'departments'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=False)

    # Relations
    users = relationship('User', back_populates='department')
