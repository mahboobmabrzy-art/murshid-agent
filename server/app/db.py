import os
from sqlalchemy import create_engine, Column, String, Integer, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from cryptography.fernet import Fernet
from datetime import datetime

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./db.sqlite3")
FERNET_KEY = os.getenv("FERNET_KEY")  # يجب أن يكون base64 32-byte

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Integration(Base):
    __tablename__ = "integrations"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(String, index=True)
    provider = Column(String)
    config_encrypted = Column(Text)
    last_tested = Column(DateTime, default=datetime.utcnow)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_fernet():
    if not FERNET_KEY:
        raise RuntimeError("FERNET_KEY not set")
    return Fernet(FERNET_KEY.encode())

def encrypt_config(plain: str) -> str:
    f = get_fernet()
    return f.encrypt(plain.encode()).decode()

def decrypt_config(token: str) -> str:
    f = get_fernet()
    return f.decrypt(token.encode()).decode()
