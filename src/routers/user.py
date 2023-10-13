from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from schemas import UserSchema, UserInSchema, UserUpdateSchema
from dependencies import get_db, get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from queries import user as user_queries
from models import User

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=List[UserSchema])
async def read_users(
        db: AsyncSession = Depends(get_db),
        limit: int = 100,
        skip: int = 0):
    return await user_queries.get_all(db=db, limit=limit, skip=skip)


@router.post("", response_model=UserSchema)
async def create_user(user: UserInSchema, db: AsyncSession = Depends(get_db)):
    new_user = await user_queries.get_by_email(db=db, email=user.email)

    if new_user:
        raise HTTPException(status_code=409, detail="User already exists")

    user = await user_queries.create(db=db, user_schema=user)
    return UserSchema.model_validate(user)


@router.put("", response_model=UserSchema)
async def update_user(
        user: UserUpdateSchema,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)):
    old_user = await user_queries.get_by_id(db=db, user_id=current_user.id)
    user_same_email = await user_queries.get_by_email(db=db, email=user.email)

    if user_same_email:
        if user_same_email.id == current_user.id:
            raise HTTPException(status_code=409, detail="User already has the specified email")

        raise HTTPException(status_code=409, detail="User with specified email already exists")

    old_user.name = user.name if user.name is not None else old_user.name
    old_user.email = user.email if user.email is not None else old_user.email
    old_user.is_company = user.is_company if user.is_company is not None else old_user.is_company

    new_user = await user_queries.update(db=db, user=old_user)

    return UserSchema.from_orm(new_user)

# TODO Удаление аккаунта

# TODO Изменение активности работы