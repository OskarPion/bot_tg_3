from fastapi import APIRouter, HTTPException
from typing import List
from db.models import User
from pydantic import BaseModel

router = APIRouter(prefix="/users", tags=["Users"])


class UserCreate(BaseModel):
    username: str
    data: dict = {}


class UserUpdate(BaseModel):
    username: str | None = None
    data: dict | None = None


@router.post("/", response_model=User)
async def create_user(user: UserCreate):
    return await User.objects.create(**user.dict())


@router.get("/", response_model=List[User])
async def get_users():
    return await User.objects.all()


@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int):
    user = await User.objects.get_or_none(id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=User)
async def update_user(user_id: int, user_update: UserUpdate):
    user = await User.objects.get_or_none(id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = user_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)
    await user.update()
    return user


@router.delete("/{user_id}")
async def delete_user(user_id: int):
    user = await User.objects.get_or_none(id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    await user.delete()
    return {"detail": "User deleted"}


user_router = router
