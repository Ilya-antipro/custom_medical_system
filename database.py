from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Используем SQLite для простоты и портативности
SQLALCHEMY_DATABASE_URL = "sqlite:///./smartpill.db"

# check_same_thread=False требуется только для SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """
    Зависимость для внедрения сессии базы данных в эндпоинты FastAPI.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()