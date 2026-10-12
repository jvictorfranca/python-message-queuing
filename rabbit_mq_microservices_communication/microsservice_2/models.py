from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base

class UsuarioModel(Base):
    """ User model for the 'tb_usuarios' table. """

    __tablename__ = "tb_usuarios"

    id = Column(UUID, primary_key=True, index=True)  # Unique identifier (UUID)
    nome = Column(String, nullable=False)  # User's name (required)
    email = Column(String, unique=True, nullable=False)  # Unique email address (required)