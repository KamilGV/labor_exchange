from sqlalchemy.ext.asyncio import AsyncSession
from models import Response, Job
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


async def check_user_creator_job(db: AsyncSession, job_id: int, user_id: int) -> bool:
    query = select(Job).where(Job.id == job_id, Job.user_id == user_id).limit(1)
    res = await db.execute(query)
    return False if res.scalars().first() is None else True
