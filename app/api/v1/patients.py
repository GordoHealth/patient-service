from datetime import date
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, status, Depends

from app.db.mappers.patient import PatientMapper
from app.db.models import PatientStatus
from app.schemas.patient import Patient, PatientCreate, PatientSearch, PatientUpdate
from app.schemas.pagination import PaginationParams, PaginatedResponse

router = APIRouter(
    prefix="/patients",
    tags=["patients"],
)


@router.get(
    "",
    response_model=PaginatedResponse[Patient],
    summary="Search patients",
)
def search_patients(
    pagination: PaginationParams = Depends(),
    last_name: Optional[str] = None,
    status: Optional[PatientStatus] = None,
    date_of_birth: Optional[date] = None,
):
    return PatientMapper.search(
        PatientSearch(
            last_name=last_name,
            status=status,
            date_of_birth=date_of_birth,
        ),
        pagination
    )


@router.get(
    "/{patient_id}",
    response_model=Patient,
    summary="Get patient by id",
)
def get_patient(patient_id: UUID):
    return PatientMapper.get_by_id(patient_id)


@router.post(
    "",
    response_model=Patient,
    status_code=status.HTTP_201_CREATED,
    summary="Create patient",
)
def create_patient(body: PatientCreate):
    return PatientMapper.create(body)


@router.put(
    "/{patient_id}",
    response_model=Patient,
    summary="Update patient",
)
def update_patient(patient_id: UUID, body: PatientUpdate):
    return PatientMapper.update(patient_id, body)


@router.delete(
    "/{patient_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete patient",
)
def delete_patient(patient_id: UUID):
    PatientMapper.delete(patient_id)
