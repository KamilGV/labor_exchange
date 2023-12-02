import pytest
from fastapi import status
from fixtures import UserFactory
from models import User
from schemas import UserInSchema, UserUpdateSchema


@pytest.mark.asyncio
async def test_unauthorized_access(test_app_unauthorized):
    deleted_user = await test_app_unauthorized.delete(url="/users")

    assert deleted_user.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_create_user(test_app_unauthorized):
    user = UserInSchema(
        name='User',
        email='email@mail.com',
        password='password123',
        password2='password123',
        is_company=False)

    registered_user = await test_app_unauthorized.post(url="/users", json=user.model_dump())

    assert registered_user.status_code == status.HTTP_200_OK
    assert user.name == registered_user.json()["name"]
    assert user.email == registered_user.json()["email"]


@pytest.mark.asyncio
async def test_create_user_email_validation_error(test_app_unauthorized):
    user = UserInSchema(
        name='User',
        email='email@mail.com',
        password='password123',
        password2='password123',
        is_company=False)
    user.email = "uncorrected_password"
    registered_user = await test_app_unauthorized.post(url="/users", json=user.model_dump())

    assert registered_user.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_create_user_password_validation_error(test_app_unauthorized):
    user = UserInSchema(
        name='User',
        email='email@mail.com',
        password='password',
        password2='password',
        is_company=False)
    user.password2 = 'uncorrected_password'

    registered_user = await test_app_unauthorized.post(url="/users", json=user.model_dump())

    assert registered_user.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_create_registered_user(test_app_unauthorized, sa_session):
    old_user = UserFactory.build()
    sa_session.add(old_user)
    sa_session.flush()

    new_user = UserInSchema(
        name='User',
        email=old_user.email,
        password='password123',
        password2='password123',
        is_company=False
    )

    registered_user = await test_app_unauthorized.post(url="/users", json=new_user.model_dump())

    assert registered_user.status_code == status.HTTP_409_CONFLICT


@pytest.mark.asyncio
async def test_read_users(test_app_user):
    jobs = await test_app_user.get("/users")
    assert jobs.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_update_user(test_user, test_app_user):
    updated_test_user = UserUpdateSchema(
        name='new_name',
        email='new_email@mail.com',
        is_company=True
    )

    updated_user = await test_app_user.put(url="/users", json=updated_test_user.model_dump())

    assert updated_user.status_code == status.HTTP_200_OK
    assert updated_test_user.name == updated_user.json()["name"]
    assert updated_test_user.email == updated_user.json()["email"]


@pytest.mark.asyncio
async def test_update_user_to_same_email(test_user: User, test_app_user):
    updated_test_user = UserUpdateSchema(
        name='new_name',
        email=test_user.email,
        is_company=True
    )

    updated_user = await test_app_user.put(url="/users", json=updated_test_user.model_dump())

    assert updated_user.status_code == status.HTTP_409_CONFLICT


@pytest.mark.asyncio
async def test_update_user_to_blocked_email(sa_session, test_user: User, test_app_user):
    old_user = UserFactory.build()
    sa_session.add(old_user)
    sa_session.flush()

    updated_test_user = UserUpdateSchema(
        name='new_name',
        email=old_user.email,
        is_company=True
    )

    updated_user = await test_app_user.put(url="/users", json=updated_test_user.model_dump())

    assert updated_user.status_code == status.HTTP_409_CONFLICT


@pytest.mark.asyncio
async def test_delete_user(test_app_user, test_user: User):
    deleted_user = await test_app_user.delete(url="/users")

    assert deleted_user.status_code == status.HTTP_200_OK
    assert deleted_user.json()["email"] == test_user.email

