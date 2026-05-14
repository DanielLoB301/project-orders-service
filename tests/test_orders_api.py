from orders_service.infrastructure.user_repository import SqlUserRepository
from orders_service.core.security import hash_password


def create_user_and_token(client, db_session):
    repo = SqlUserRepository(db_session)
    repo.create("admin", hash_password("admin123"))

    response = client.post(
        "/token",
        data={"username": "admin", "password": "admin123"},
    )

    return response.json()["access_token"]


def test_create_order_protected(client, db_session):
    token = create_user_and_token(client, db_session)

    response = client.post(
        "/orders/",
        json={"user_id": 1, "total": 500},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["total"] == 500


def test_create_order_without_token(client):
    response = client.post(
        "/orders/",
        json={"user_id": 1, "total": 500},
    )

    assert response.status_code == 401