from orders_service.infrastructure.user_repository import SqlUserRepository
from orders_service.core.security import hash_password


def create_test_user(db):
    repo = SqlUserRepository(db)
    repo.create("admin", hash_password("admin123"))


def test_login_success(client, db_session):
    create_test_user(db_session)

    response = client.post(
        "/token",
        data={"username": "admin", "password": "admin123"},
    )

    assert response.status_code == 200
    assert "access_token" in response.json()