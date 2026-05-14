from sqlalchemy.orm import Session

from orders_service.db.database import SessionLocal
from orders_service.infrastructure.user_repository import SqlUserRepository
from orders_service.core.security import hash_password


def main() -> None:
    db: Session = SessionLocal()
    repo = SqlUserRepository(db)

    repo.create(
        username="admin",
        hashed_password=hash_password("admin123"),
    )

    print("User created")


if __name__ == "__main__":
    main()