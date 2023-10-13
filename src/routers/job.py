from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies import get_db, get_current_user
from typing import List
from queries import job as job_queries
from schemas import JobSchema, JobInSchema
from models import Job, User


router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("", response_model=List[JobSchema])
async def read_jobs(
        db: AsyncSession = Depends(get_db),
        limit: int = 100,
        skip: int = 0):
    return await job_queries.get_all_jobs(db=db, limit=limit, skip=skip)


@router.post("", response_model=JobSchema)
async def create_job(
        job: JobInSchema,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)):
    if not current_user.is_company:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized access")

    new_job = await job_queries.create_job(db=db, job_schema=job, user_id=current_user.id)
    return JobSchema.model_validate(new_job)

# TODO Update delete(В бд остаются)