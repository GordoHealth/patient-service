from typing import Optional
from uuid import UUID

from fastapi import APIRouter, status, Depends

from app.db.mappers.patient_medication import PatientMedicationMapper
from app.schemas.patient_medication import (
    PatientMedication,
    PatientMedicationCreate,
    PatientMedicationSearch,
    PatientMedicationUpdate,
)
from app.schemas.pagination import PaginationParams, PaginatedResponse

router = APIRouter(
    prefix="/patient-medications",
    tags=["patient-medications"],
)


@router.get(
    "",
    response_model=PaginatedResponse[PatientMedication],
    summary="Search patient medications",
)
def search_patient_medications(
    pagination: PaginationParams = Depends(),
    patient_id: Optional[UUID] = None,
    medication_id: Optional[UUID] = None,
    is_discontinued: Optional[bool] = None,
):
    return PatientMedicationMapper.search(
        PatientMedicationSearch(
            patient_id=patient_id,
            medication_id=medication_id,
            is_discontinued=is_discontinued,
        ),
        pagination
    )


@router.get(
    "/{patient_medication_id}",
    response_model=PatientMedication,
    summary="Get patient medication by id",
)
def get_patient_medication(patient_medication_id: UUID):
    return PatientMedicationMapper.get_by_id(patient_medication_id)


@router.post(
    "",
    response_model=PatientMedication,
    status_code=status.HTTP_201_CREATED,
    summary="Create patient medication",
)
def create_patient_medication(body: PatientMedicationCreate):
    return PatientMedicationMapper.create(body)


@router.put(
    "/{patient_medication_id}",
    response_model=PatientMedication,
    summary="Update patient medication",
)
def update_patient_medication(
    patient_medication_id: UUID,
    body: PatientMedicationUpdate,
):
    return PatientMedicationMapper.update(patient_medication_id, body)


@router.delete(
    "/{patient_medication_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete patient medication",
)
def delete_patient_medication(patient_medication_id: UUID):
    PatientMedicationMapper.delete(patient_medication_id)
