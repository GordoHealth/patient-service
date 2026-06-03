from typing import Optional
from uuid import UUID

from fastapi import APIRouter, status

from app.db.mappers.clinical_chart import ClinicalChartMapper
from app.schemas.clinical_chart import (
    ClinicalChart,
    ClinicalChartCreate,
    ClinicalChartSearch,
    ClinicalChartUpdate,
)

router = APIRouter(
    prefix="/clinical-charts",
    tags=["clinical-charts"],
)


@router.get(
    "",
    response_model=list[ClinicalChart],
    summary="Search clinical charts",
)
def search_clinical_charts(patient_id: Optional[UUID] = None):
    return ClinicalChartMapper.search(ClinicalChartSearch(patient_id=patient_id))


@router.get(
    "/{clinical_chart_id}",
    response_model=ClinicalChart,
    summary="Get clinical chart by id",
)
def get_clinical_chart(clinical_chart_id: UUID):
    return ClinicalChartMapper.get_by_id(clinical_chart_id)


@router.post(
    "",
    response_model=ClinicalChart,
    status_code=status.HTTP_201_CREATED,
    summary="Create clinical chart",
)
def create_clinical_chart(body: ClinicalChartCreate):
    return ClinicalChartMapper.create(body)


@router.put(
    "/{clinical_chart_id}",
    response_model=ClinicalChart,
    summary="Update clinical chart",
)
def update_clinical_chart(clinical_chart_id: UUID, body: ClinicalChartUpdate):
    return ClinicalChartMapper.update(clinical_chart_id, body)


@router.delete(
    "/{clinical_chart_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete clinical chart",
)
def delete_clinical_chart(clinical_chart_id: UUID):
    ClinicalChartMapper.delete(clinical_chart_id)
