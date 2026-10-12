from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Obtém a URL do banco de dados da variável de ambiente
DATABASE_URL = os.environ.get("DATABASE_URL_MICROSSERVICO_1")

# Cria a engine para gerenciar a conexão com o banco
engine = create_engine(DATABASE_URL)

# Configura a sessão do SQLAlchemy
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define a classe base para os modelos ORM
Base = declarative_base()

def get_session():
    """ Gera uma sessão de banco de dados e garante seu fechamento. """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
