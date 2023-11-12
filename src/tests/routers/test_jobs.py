import pytest
from fastapi import status

from fixtures import JobFactory, UserFactory
from models import User
from schemas import JobInSchema, JobUpdateSchema


@pytest.mark.asyncio
async def test_create_job_by_company(test_app_company):
    job = JobInSchema(
        title="Work",
        description="Working",
        salary_from=1000,
        salary_to=30000,
        is_active=True
    )

    created_job = await test_app_company.post(url="/jobs", json=job.model_dump())
    assert created_job.status_code == status.HTTP_200_OK
    assert created_job.json()["title"] == job.title


@pytest.mark.asyncio
async def test_create_job_by_user(test_app_user, test_company, test_user):
    job = JobInSchema(
        title="Work",
        description="Working",
        salary_from=1000,
        salary_to=30000,
        is_active=True
    )

    created_job = await test_app_user.post(url="/jobs", json=job.model_dump())
    assert created_job.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_create_job_wrong_salary_range(test_app_company):
    job = JobInSchema(
        title="Work",
        description="Working",
        salary_from=1000,
        salary_to=20000,
        is_active=True
    )
    job.salary_to = 0

    created_job = await test_app_company.post(url="/jobs", json=job.model_dump())

    assert created_job.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_read_job(test_app_unauthorized):
    jobs = await test_app_unauthorized.get(url="/jobs")
    assert jobs.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_update_job(sa_session, test_app_company, test_company: User):
    job = JobFactory.build()
    job.user_id = test_company.id
    job.is_active = True
    sa_session.add(job)
    sa_session.flush()

    update_job = JobUpdateSchema(
        id=job.id,
        title='updated_title',
        description='updated_decryption',
        salary_from=1000,
        salary_to=2000,
    )

    job = await test_app_company.put(url="/jobs", json=update_job.model_dump())

    assert job.status_code == status.HTTP_200_OK
    assert job.json()["title"] == update_job.title
    assert job.json()["salary_from"] == update_job.salary_from


@pytest.mark.asyncio
async def test_update_job_by_not_creator(sa_session, test_app_company, test_company: User):
    user = UserFactory.build()
    user.is_company = True
    sa_session.add(user)
    sa_session.flush()

    job = JobFactory.build()
    job.user_id = user.id
    sa_session.add(job)
    sa_session.flush()

    update_job = JobUpdateSchema(
        id=job.id,
        title='updated_title',
        description='updated_decryption',
        salary_from=1000,
        salary_to=2000,
    )

    job = await test_app_company.put(url="/jobs", json=update_job.model_dump())

    assert job.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_update_not_active_job(sa_session, test_app_company, test_company: User):
    job = JobFactory.build()
    job.user_id = test_company.id
    job.is_active = False
    sa_session.add(job)
    sa_session.flush()

    update_job = JobUpdateSchema(
        id=job.id,
        title='updated_title',
        description='updated_decryption',
        salary_from=1000,
        salary_to=2000,
    )

    job = await test_app_company.put(url="/jobs", json=update_job.model_dump())

    assert job.status_code == status.HTTP_409_CONFLICT


@pytest.mark.asyncio
async def test_update_job_wrong_salary_range(sa_session, test_app_company, test_company: User):
    job = JobFactory.build()
    job.user_id = test_company.id
    sa_session.add(job)
    sa_session.flush()

    update_job = JobUpdateSchema(
        id=job.id,
        title='updated_title',
        description='updated_decryption',
        salary_from=1000,
        salary_to=2000,
    )
    update_job.salary_to = 0
    job = await test_app_company.put(url="/jobs", json=update_job.model_dump())

    assert job.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_delete_job(sa_session, test_app_company, test_company: User):
    job = JobFactory.build()
    job.user_id = test_company.id
    job.is_active = True
    sa_session.add(job)
    sa_session.flush()

    job = await test_app_company.delete(url=f"/jobs?job_id={job.id}")

    assert job.status_code == status.HTTP_200_OK
    assert job.json()["is_active"] is False


@pytest.mark.asyncio
async def test_delete_job_by_not_creator(sa_session, test_app_user, test_company: User):
    user = UserFactory.build()
    user.is_company = True
    sa_session.add(user)
    sa_session.flush()

    job = JobFactory.build()
    job.user_id = user.id
    job.is_active = True
    sa_session.add(job)
    sa_session.flush()

    job = await test_app_user.delete(url=f"/jobs?job_id={job.id}")

    assert job.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_delete_not_active_job(sa_session, test_app_company, test_company: User):
    job = JobFactory.build()
    job.user_id = test_company.id
    job.is_active = False
    sa_session.add(job)
    sa_session.flush()

    job = await test_app_company.delete(url=f"/jobs?job_id={job.id}")

    assert job.status_code == status.HTTP_409_CONFLICT
