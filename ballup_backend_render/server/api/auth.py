from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session
from server.database import get_db
from server.models.user import User
from server.services.telegram_auth import validate_init_data

router = APIRouter(prefix="/auth", tags=["auth"])

class TelegramAuthRequest(BaseModel):
    init_data: str

@router.post("/telegram")
def telegram_auth(payload: TelegramAuthRequest, db: Session = Depends(get_db)):
    tg = validate_init_data(payload.init_data)
    user = db.scalar(select(User).where(User.telegram_id == tg["id"]))
    if user is None:
        user = User(telegram_id=tg["id"])
        db.add(user)
    user.username = tg.get("username")
    user.first_name = tg.get("first_name")
    user.last_name = tg.get("last_name")
    db.commit()
    return {"telegram_id": user.telegram_id, "authenticated": True}
