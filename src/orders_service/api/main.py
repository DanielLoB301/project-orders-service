from typing import Dict

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from orders_service.core.security import verify_password, create_access_token
from orders_service.infrastructure.user_repository import SqlUserRepository
from orders_service.db.database import SessionLocal
from orders_service.api.routers import orders

app = FastAPI(title="Orders Service")

app.include_router(orders.router)


@app.get("/")
def root() -> Dict[str, str]:
    return {"message": "Orders Service running"}


@app.get("/health")
def health_check() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/token")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Dict[str, str]:
    db: Session = SessionLocal()
    repo = SqlUserRepository(db)

    user = repo.get_by_username(form_data.username)

    if not user or not verify_password(
        form_data.password, user.hashed_password
    ):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token: str = create_access_token({"sub": user.username})

    db.close()

    return {"access_token": access_token, "token_type": "bearer"}