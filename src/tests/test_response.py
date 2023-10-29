import pytest
from models import User
from queries import response as response_query
from fixtures import ResponseFactory, JobFactory, UserFactory
from schemas import ResponseInSchema


@pytest.mark.asyncio
async def test_response_job(sa_session, test_user: User):
    user_creator_job = UserFactory.build()
    sa_session.add(user_creator_job)

    job = JobFactory.build()
    job.user_id = user_creator_job.id
    sa_session.add(job)
    sa_session.flush()

    response_in = ResponseInSchema(
        job_id=job.id,
        message='Walk is not work, walk is Гулять')

    response_out = await response_query.response_job(db=sa_session, response=response_in, user_id=test_user.id)
    assert response_out
    assert response_out.job_id == job.id
    assert response_out.user_id == test_user.id


@pytest.mark.asyncio
async def test_get_responses_by_job_id(sa_session, test_user: User):
    user_creator_job = UserFactory.build()
    sa_session.add(user_creator_job)

    job = JobFactory.build()
    job.user_id = user_creator_job.id
    sa_session.add(job)
    sa_session.flush()

    response_in = ResponseInSchema(
        job_id=job.id,
        message='Walk is not work, walk is Гулять')
    response_out = await response_query.response_job(db=sa_session, response=response_in, user_id=test_user.id)
    responses = await response_query.get_responses_by_job_id(db=sa_session, job_id=job.id)
    assert len(responses) == 1
    assert responses[0].job_id == job.id
    assert responses[0].id == response_out.id
    assert responses[0].user_id == test_user.id


@pytest.mark.asyncio
async def test_delete_response(sa_session, test_user: User):
    user_creator_job = UserFactory.build()
    sa_session.add(user_creator_job)

    job = JobFactory.build()
    job.user_id = user_creator_job.id
    sa_session.add(job)
    sa_session.flush()

    response_in = ResponseInSchema(
        job_id=job.id,
        message='Walk is not work, walk is Гулять')
    response_out = await response_query.response_job(db=sa_session, response=response_in, user_id=test_user.id)

    deleted_response = await response_query.delete_response(db=sa_session, response=response_out)
    assert deleted_response.id == response_out.id

    deleted_response = await response_query.get_responses_by_job_id(db=sa_session, job_id=job.id)

    assert len(deleted_response) == 0
