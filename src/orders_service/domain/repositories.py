from typing import Protocol
from orders_service.domain.entities import Order


class OrderRepository(Protocol):
    def save(self, order: Order) -> Order:
        ...

    def list(self) -> list[Order]:
        ...