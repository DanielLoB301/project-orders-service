from orders_service.domain.entities import Order
from orders_service.domain.notification_port import NotificationPort
from orders_service.domain.repositories import OrderRepository


class CreateOrderUseCase:
    def __init__(
        self,
        repository: OrderRepository,
        notifier: NotificationPort,
    ):
        self.repository = repository
        self.notifier = notifier

    def execute(self, user_id: int, total: float) -> Order:
        if total <= 0:
            raise ValueError("Total must be positive")

        if total > 10000:
            raise ValueError("Total exceeds allowed limit")

        order = Order(id=None, user_id=user_id, total=total)

        saved_order = self.repository.save(order)

        self.notifier.notify(f"Order created with id {saved_order.id}")

        return saved_order
