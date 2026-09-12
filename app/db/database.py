import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Cambiar en produccion
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://plurione_user:secretpassword@localhost:5432/Sentiment_db")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()