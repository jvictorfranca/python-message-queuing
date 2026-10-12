from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base

class UsuarioModel(Base):
    """ Modelo de usuário para a tabela 'tb_usuarios'. """
    
    __tablename__ = "tb_usuarios"

    id = Column(UUID, primary_key=True, index=True)  # Identificador único (UUID)
    nome = Column(String, nullable=False)  # Nome do usuário (obrigatório)
    email = Column(String, unique=True, nullable=False)  # E-mail único (obrigatório)
