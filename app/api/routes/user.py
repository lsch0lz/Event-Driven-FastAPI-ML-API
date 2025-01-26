import uuid
from fastapi import APIRouter, HTTPException, Depends

from app.core.auth.security import get_password_hash
from app.core.db.database import SessionDependency
from app.core.db.models import User

router = APIRouter(prefix="/user", tags=["user"])


@router.post("/create")
async def create_user(user: User, session: SessionDependency) -> None:
    user_model = User(
        id=uuid.uuid4(),
        username=user.username,
        password=get_password_hash(user.password),
        email=user.email,
        full_name=user.full_name,
        disabled=user.disabled
    )
    session.add(user_model)
    session.commit()
    session.refresh(user_model)
