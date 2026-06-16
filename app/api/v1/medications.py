from typing import Optional
from uuid import UUID

from fastapi import APIRouter, status, Depends

from app.db.mappers.medication import MedicationMapper
from app.schemas.medication import (
    Medication,
    MedicationCreate,
    MedicationSearch,
    MedicationUpdate,
)
from app.schemas.pagination import PaginationParams, PaginatedResponse

router = APIRouter(
    prefix="/medications",
    tags=["medications"],
)


@router.get(
    "",
    response_model=PaginatedResponse[Medication],
    summary="Search medications",
)
def search_medications(pagination: PaginationParams = Depends(), name: Optional[str] = None):
    if name is not None:
        return MedicationMapper.search_by_name(name)
    return MedicationMapper.search(MedicationSearch(), pagination)


@router.get(
    "/{medication_id}",
    response_model=Medication,
    summary="Get medication by id",
)
def get_medication(medication_id: UUID):
    return MedicationMapper.get_by_id(medication_id)


@router.post(
    "",
    response_model=Medication,
    status_code=status.HTTP_201_CREATED,
    summary="Create medication",
)
def create_medication(body: MedicationCreate):
    return MedicationMapper.create(body)


@router.put(
    "/{medication_id}",
    response_model=Medication,
    summary="Update medication",
)
def update_medication(medication_id: UUID, body: MedicationUpdate):
    return MedicationMapper.update(medication_id, body)


@router.delete(
    "/{medication_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete medication",
)
def delete_medication(medication_id: UUID):
    MedicationMapper.delete(medication_id)
