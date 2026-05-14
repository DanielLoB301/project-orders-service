from orders_service.core.security import hash_password
from orders_service.db.database import SessionLocal
from orders_service.infrastructure.user_repository import SqlUserRepository


def main():
    db = SessionLocal()
    repo = SqlUserRepository(db)

    repo.create(
        username="admin",
        hashed_password=hash_password("admin123"),
    )

    print("User created")


if __name__ == "__main__":
    main()
