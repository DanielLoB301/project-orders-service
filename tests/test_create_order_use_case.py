import pytest

from orders_service.application.use_cases import CreateOrderUseCase
from orders_service.domain.entities import Order
from orders_service.domain.notification_port import NotificationPort


class FakeRepository:
    def __init__(self):
        self._orders = []
        self._id = 1

    def save(self, order: Order) -> Order:
        order.id = self._id
        self._orders.append(order)
        self._id += 1
        return order

    def list(self):
        return self._orders


class FakeNotifier(NotificationPort):
    def __init__(self):
        self.messages = []

    def notify(self, message: str) -> None:
        self.messages.append(message)


def test_create_order_success():
    repo = FakeRepository()
    notifier = FakeNotifier()

    use_case = CreateOrderUseCase(repo, notifier)

    order = use_case.execute(user_id=1, total=100)

    assert order.id == 1
    assert order.user_id == 1
    assert order.total == 100
    assert len(notifier.messages) == 1


def test_create_order_negative_total():
    repo = FakeRepository()
    notifier = FakeNotifier()

    use_case = CreateOrderUseCase(repo, notifier)

    with pytest.raises(ValueError):
        use_case.execute(user_id=1, total=-10)


def test_create_order_exceeds_limit():
    repo = FakeRepository()
    notifier = FakeNotifier()

    use_case = CreateOrderUseCase(repo, notifier)

    with pytest.raises(ValueError):
        use_case.execute(user_id=1, total=20000)
