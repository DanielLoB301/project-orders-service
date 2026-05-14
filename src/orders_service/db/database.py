from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE_URL = "sqlite:///./orders.db"


class Base(DeclarativeBase):
    pass


engine = create_engine(
    DATABASE_URL,
    echo=True,  # Muestra SQL en consola (útil en desarrollo)
)

SessionLocal = sessionmaker(bind=engine)
