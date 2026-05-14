from typing import Protocol


class NotificationPort(Protocol):
    def notify(self, message: str) -> None:
        ...
