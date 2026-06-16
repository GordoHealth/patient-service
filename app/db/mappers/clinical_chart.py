from app.db.mappers.base_mapper import BaseMapper
from app.db.models import ClinicalChart
from app.schemas.clinical_chart import (
    ClinicalChartCreate,
    ClinicalChartSearch,
    ClinicalChartUpdate,
)


class ClinicalChartMapper(
    BaseMapper[ClinicalChart, ClinicalChartCreate, ClinicalChartUpdate, ClinicalChartSearch]
):
    @classmethod
    def model(cls):
        return ClinicalChart
