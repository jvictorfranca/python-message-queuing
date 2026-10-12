from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Retrieves the database URL from the environment variable
DATABASE_URL = os.environ.get("DATABASE_URL_MICROSSERVICO_2")

# Creates the engine to manage the database connection
engine = create_engine(DATABASE_URL)

# Configures the SQLAlchemy session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Defines the base class for ORM models
Base = declarative_base()

def get_session():
    """Generates a database session and ensures it is closed."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()