from fastapi import APIRouter, Depends, HTTPException, status
from dependencies import get_db, get_current_user
from models import User, Response
from queries import response as response_queries
from queries.job import get_job_by_id
from schemas import ResponseSchema, ResponseInSchema
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/response", tags=["response"])


@router.get("", response_model=list[ResponseSchema])
async def read_responses_by_job_id(
        job_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)):

    check = response_queries.check_user_creator_job(job_id=job_id, user=current_user)
    if not current_user.is_company or not check:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized access")

    responses = await response_queries.get_responses_by_job_id(db=db, job_id=job_id)
    return responses


@router.post("", response_model=ResponseSchema)
async def post_response(
        response: ResponseInSchema,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)):

    if current_user.is_company:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized access")

    if response_queries.get_response_user_job(job_id=response.job_id, user=current_user):
        raise HTTPException(status_code=409, detail="Response is exist")

    job = await get_job_by_id(db=db, job_id=response.job_id)
    if not job:
        raise HTTPException(status_code=406, detail="Job not exist")
    if not job.is_active:
        raise HTTPException(status_code=409, detail="Job is not active")

    response = await response_queries.response_job(db=db, response=response, user_id=current_user.id)
    return ResponseSchema.model_validate(response)


@router.delete("", response_model=ResponseSchema)
async def delete_response(
        job_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)):

    if current_user.is_company:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized access")

    response = response_queries.get_response_user_job(job_id=job_id, user=current_user)
    if not response:
        raise HTTPException(status_code=409, detail="Response not exist")

    response = await response_queries.delete_response(db=db, response=response)
    return response
