from http.client import HTTPException

from fastapi import FastAPI

from orders_service.api.routers import orders
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

from orders_service.core.security import verify_password, create_access_token
from orders_service.infrastructure.user_repository import SqlUserRepository
from orders_service.db.database import SessionLocal

app = FastAPI(title="Orders Service")

app.include_router(orders.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"message": "Orders Service running"}

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    db = SessionLocal()
    repo = SqlUserRepository(db)

    user = repo.get_by_username(form_data.username)

    if not user or not verify_password(
        form_data.password, user.hashed_password
    ):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": user.username})

    return {"access_token": access_token, "token_type": "bearer"}