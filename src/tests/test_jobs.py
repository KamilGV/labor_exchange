import pytest

from models import User
from queries import job as job_query
from fixtures.jobs import JobFactory
from schemas import JobInSchema


@pytest.mark.asyncio
async def test_create(sa_session, test_user: User):
    job = JobInSchema(
        title='Work',
        description='Работа не волк, работа - work',
        salary_from=100,
        salary_to=199.99,
        is_active=True)

    new_job = await job_query.create_job(
        db=sa_session,
        job_schema=job,
        user_id=test_user.id)

    assert new_job is not None
    assert new_job.title == 'Work'
    assert new_job.salary_from == 100.00


@pytest.mark.asyncio
async def test_get_all(sa_session, test_user: User):
    job = JobFactory.build()
    job.user_id = test_user.id
    sa_session.add(job)
    sa_session.flush()

    all_jobs = await job_query.get_all_jobs(sa_session)
    assert all_jobs
    assert len(all_jobs) == 1
    assert all_jobs[0] == job


@pytest.mark.asyncio
async def test_get_by_id(sa_session, test_user: User):
    job = JobFactory.build()
    job.user_id = test_user.id
    sa_session.add(job)
    sa_session.flush()

    current_job = await job_query.get_job_by_id(db=sa_session,job_id=job.id)

    assert current_job is not None
    assert current_job.id == job.id


@pytest.mark.asyncio
async def test_update(sa_session, test_user: User):
    job = JobFactory.build()
    job.user_id = test_user.id
    sa_session.add(job)
    sa_session.flush()

    job.title = "updated_title"
    updated_job = await job_query.update(db=sa_session, job=job)
    assert job.id == updated_job.id
    assert updated_job.title == "updated_title"
