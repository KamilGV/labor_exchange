import pytest
from fastapi import status

from fixtures import JobFactory, ResponseFactory
from models import User
from schemas import ResponseInSchema


@pytest.mark.asyncio
async def test_read_responses_by_job_id(sa_session, test_app_company, test_user: User, test_company: User):
    job = JobFactory.build()
    job.user_id = test_company.id
    sa_session.add(job)
    sa_session.flush()

    response = ResponseFactory.build()
    response.job_id = job.id
    response.user_id = test_user.id
    sa_session.add(response)
    sa_session.flush()

    responses = await test_app_company.get(url=f"/response?job_id={job.id}")

    assert responses.status_code == status.HTTP_200_OK
    assert len(responses.json()) == 1


@pytest.mark.asyncio
async def test_read_responses_by_job_id_not_creator(sa_session, test_app_user, test_user: User, test_company: User):
    job = JobFactory.build()
    job.user_id = test_company.id
    sa_session.add(job)
    sa_session.flush()

    responses = await test_app_user.get(url=f"/response?job_id={job.id}")

    assert responses.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_post_response(sa_session, test_app_user, test_user: User, test_company: User):
    job = JobFactory.build()
    job.is_active = True
    job.user_id = test_company.id
    sa_session.add(job)
    sa_session.flush()

    response = ResponseInSchema(
        job_id=job.id,
        message="Text"
    )

    response = await test_app_user.post(url="/response", json=response.model_dump())

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["job_id"] == job.id


@pytest.mark.asyncio
async def test_post_response_by_not_active_job(sa_session, test_app_user, test_user: User, test_company: User):
    job = JobFactory.build()
    job.is_active = False
    job.user_id = test_company.id
    sa_session.add(job)
    sa_session.flush()

    response = ResponseInSchema(
        job_id=job.id,
        message="Text"
    )

    response = await test_app_user.post(url="/response", json=response.model_dump())

    assert response.status_code == status.HTTP_409_CONFLICT


@pytest.mark.asyncio
async def test_post_response_as_company(sa_session, test_app_company, test_user: User, test_company: User):
    job = JobFactory.build()
    job.is_active = False
    job.user_id = test_company.id
    sa_session.add(job)
    sa_session.flush()

    response = ResponseInSchema(
        job_id=job.id,
        message="Text"
    )

    response = await test_app_company.post(url="/response", json=response.model_dump())

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_post_response_by_not_existing_job(sa_session, test_app_user, test_user: User, test_company: User):
    response = ResponseInSchema(
        job_id=10,
        message="Text"
    )

    response = await test_app_user.post(url="/response", json=response.model_dump())

    assert response.status_code == status.HTTP_406_NOT_ACCEPTABLE


@pytest.mark.asyncio
async def test_delete_response(sa_session, test_app_user, test_user: User, test_company: User):
    job = JobFactory.build()
    job.user_id = test_company.id
    sa_session.add(job)
    sa_session.flush()

    response = ResponseFactory.build()
    response.job_id = job.id
    response.user_id = test_user.id
    sa_session.add(response)
    sa_session.flush()

    responses = await test_app_user.delete(url=f"/response?job_id={response.id}")

    assert responses.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_delete_response_as_company(sa_session, test_app_company, test_user: User, test_company: User):
    job = JobFactory.build()
    job.user_id = test_company.id
    sa_session.add(job)
    sa_session.flush()

    response = ResponseFactory.build()
    response.job_id = job.id
    response.user_id = test_user.id
    sa_session.add(response)
    sa_session.flush()

    responses = await test_app_company.delete(url=f"/response?job_id={response.id}")

    assert responses.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_delete_not_existing_response(sa_session, test_app_user, test_user: User, test_company: User):
    responses = await test_app_user.delete(url=f"/response?job_id={2}")

    assert responses.status_code == status.HTTP_409_CONFLICT
