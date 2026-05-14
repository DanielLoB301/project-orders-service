from http.client import HTTPException

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from orders_service.api.auth import get_db
from orders_service.api.routers import orders
from orders_service.core.security import create_access_token, verify_password
from orders_service.infrastructure.user_repository import SqlUserRepository

app = FastAPI(title="Orders Service")

app.include_router(orders.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"message": "Orders Service running"}

@app.post("/token")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    repo = SqlUserRepository(db)

    user = repo.get_by_username(form_data.username)

    if not user or not verify_password(
        form_data.password, user.hashed_password
    ):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": user.username})

    return {"access_token": access_token, "token_type": "bearer"}
