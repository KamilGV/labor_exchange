from fastapi import APIRouter, Depends, HTTPException, status
from dependencies import get_db, get_current_user
from models import User, Response
from queries.response import get_responses_by_job_id, response_job, check_user_creator_job
from queries.job import get_job_by_id
from schemas import ResponseSchema, ResponseInSchema
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/response", tags=["response"])

#Какой код у ошибок?

# TODO
# TODO Проверка через релашионшип
@router.get("", response_model=list[ResponseSchema])
async def read_responses_by_job_id(
        job_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)):
    # TODO Поправить
    check = check_user_creator_job(job_id=job_id, user=current_user)
    #print(current_user.jobs)
    #for job in current_user.jobs:

    if not current_user.is_company or not check:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized access")

    responses = await get_responses_by_job_id(db=db, job_id=job_id)

    return responses


@router.post("", response_model=ResponseSchema)
async def post_response(
        response: ResponseInSchema,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)):

    if current_user.is_company:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized access")

    job = await get_job_by_id(db=db, job_id=response.job_id)
    if not job:
        raise HTTPException(status_code=409, detail="Job is not exist")
    if not job.is_active:
        raise HTTPException(status_code=409, detail="Job is not active")

    response = await response_job(db=db, response=response, user_id=current_user.id)
    return ResponseSchema.model_validate(response)

# TODO создать ендпоинт на Удаление  отклика
# TODO ошибка если отклик уже был
# TODO convential commits, pull request