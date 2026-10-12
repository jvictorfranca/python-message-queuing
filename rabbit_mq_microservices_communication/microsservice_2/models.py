from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base

class UserModel(Base):
    """User model for the 'users' table."""

    __tablename__ = "users"

    id = Column(UUID, primary_key=True, index=True)  # Unique identifier (UUID)
    name = Column(String, nullable=False)  # User's name (required)
    email = Column(String, unique=True, nullable=False)  # Unique email address (required)