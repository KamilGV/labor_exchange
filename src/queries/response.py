from sqlalchemy.ext.asyncio import AsyncSession
from models import Response, Job, User
from sqlalchemy import select
from typing import List
from schemas import ResponseSchema, ResponseInSchema


async def response_job(db: AsyncSession, response: ResponseInSchema, user_id: int) -> Response:

    response = Response(
        user_id=user_id,
        job_id=response.job_id,
        message=response.message
    )

    db.add(response)
    await db.commit()
    await db.refresh(response)
    return response


async def get_responses_by_job_id(db: AsyncSession, job_id: int) -> List[Response]:
    query = select(Response).where(Response.job_id == job_id)
    res = await db.execute(query)
    return res.scalars().all()


def check_user_creator_job(job_id: int, user: User) -> bool:
    for job in user.jobs:
        if job.id == job_id:
            return True
    return False
