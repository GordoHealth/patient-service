from typing import Optional
from uuid import UUID

from fastapi import APIRouter, status, Depends

from app.db.mappers.care_plan import CarePlanMapper
from app.schemas.care_plan import CarePlan, CarePlanCreate, CarePlanSearch, CarePlanUpdate
from app.schemas.pagination import PaginationParams, PaginatedResponse

router = APIRouter(
    prefix="/care-plans",
    tags=["care-plans"],
)


@router.get(
    "",
    response_model=PaginatedResponse[CarePlan],
    summary="Search care plans",
)
def search_care_plans(
    pagination: PaginationParams = Depends(),
    patient_id: Optional[UUID] = None,
    ordering_physician_id: Optional[UUID] = None,
):
    return CarePlanMapper.search(
        CarePlanSearch(
            patient_id=patient_id,
            ordering_physician_id=ordering_physician_id,
        ),
        pagination
    )


@router.get(
    "/{care_plan_id}",
    response_model=CarePlan,
    summary="Get care plan by id",
)
def get_care_plan(care_plan_id: UUID):
    return CarePlanMapper.get_by_id(care_plan_id)


@router.post(
    "",
    response_model=CarePlan,
    status_code=status.HTTP_201_CREATED,
    summary="Create care plan",
)
def create_care_plan(body: CarePlanCreate):
    return CarePlanMapper.create(body)


@router.put(
    "/{care_plan_id}",
    response_model=CarePlan,
    summary="Update care plan",
)
def update_care_plan(care_plan_id: UUID, body: CarePlanUpdate):
    return CarePlanMapper.update(care_plan_id, body)


@router.delete(
    "/{care_plan_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete care plan",
)
def delete_care_plan(care_plan_id: UUID):
    CarePlanMapper.delete(care_plan_id)
