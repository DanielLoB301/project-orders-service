from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from sqlalchemy.orm import Session

from orders_service.core.security import SECRET_KEY, ALGORITHM
from orders_service.db.database import SessionLocal
from orders_service.infrastructure.user_repository import SqlUserRepository
from orders_service.api.dependencies import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    repo = SqlUserRepository(db)
    user = repo.get_by_username(username)

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user