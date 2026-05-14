from orders_service.db.database import engine
from orders_service.db.models import Base


def init_db() -> None:
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()