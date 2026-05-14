from sqlalchemy.orm import Session

from orders_service.db.models import UserORM


class SqlUserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_username(self, username: str) -> UserORM | None:
        return (
            self.db.query(UserORM)
            .filter(UserORM.username == username)
            .first()
        )

    def create(self, username: str, hashed_password: str) -> UserORM:
        user = UserORM(
            username=username,
            hashed_password=hashed_password,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user