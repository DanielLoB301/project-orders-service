from orders_service.db.database import SessionLocal
from orders_service.db.models import Base
from orders_service.db.database import engine
from orders_service.domain.entities import Order
from orders_service.infrastructure.sql_repository import SqlOrderRepository


def setup_module():
    Base.metadata.create_all(bind=engine)


def teardown_module():
    Base.metadata.drop_all(bind=engine)


def test_sql_repository_save_and_list():
    db = SessionLocal()
    repo = SqlOrderRepository(db)

    order = Order(id=None, user_id=1, total=100)

    saved = repo.save(order)

    assert saved.id is not None

    orders = repo.list()

    assert len(orders) >= 1

    db.close()