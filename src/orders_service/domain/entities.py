from dataclasses import dataclass


@dataclass
class Order:
    id: int | None
    user_id: int
    total: float
