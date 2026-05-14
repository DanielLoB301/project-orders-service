from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from orders_service.api.schemas import OrderCreate, OrderResponse
from orders_service.application.use_cases import CreateOrderUseCase
from orders_service.infrastructure.sql_repository import SqlOrderRepository
from orders_service.db.database import SessionLocal
from orders_service.domain.notification_port import NotificationPort
from orders_service.api.auth import get_current_user
from orders_service.api.dependencies import get_db

router = APIRouter(prefix="/orders", tags=["orders"])




# Notificador simple
class ConsoleNotifier(NotificationPort):
    def notify(self, message: str) -> None:
        print(message)


@router.post("/", response_model=OrderResponse)
def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    repo = SqlOrderRepository(db)
    notifier = ConsoleNotifier()

    use_case = CreateOrderUseCase(repo, notifier)

    try:
        result = use_case.execute(order.user_id, order.total)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return result