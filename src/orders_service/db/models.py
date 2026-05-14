from sqlalchemy import Integer, Float
from sqlalchemy.orm import Mapped, mapped_column

from orders_service.db.database import Base


class OrderORM(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer)
    total: Mapped[float] = mapped_column(Float)