from sqlalchemy.orm import Session

from orders_service.db.models import OrderORM
from orders_service.domain.entities import Order
from orders_service.domain.repositories import OrderRepository


class SqlOrderRepository(OrderRepository):
    def __init__(self, db: Session):
        self.db = db

    def save(self, order: Order) -> Order:
        orm_order = OrderORM(
            user_id=order.user_id,
            total=order.total,
        )

        self.db.add(orm_order)
        self.db.commit()
        self.db.refresh(orm_order)

        return Order(
            id=orm_order.id,
            user_id=orm_order.user_id,
            total=orm_order.total,
        )

    def list(self) -> list[Order]:
        rows = self.db.query(OrderORM).all()

        return [
            Order(
                id=row.id,
                user_id=row.user_id,
                total=row.total,
            )
            for row in rows
        ]
