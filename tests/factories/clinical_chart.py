from uuid import uuid4

from app.db.models import ClinicalChart
from app.schemas.clinical_chart import ClinicalChartCreate
from tests.factories.audit import audit_kwargs
from tests.factories.base_factory import FakerFactory


class ClinicalChartFactory(FakerFactory):
    def __init__(self, faker_instance=None):
        super().__init__(faker_instance)
        self._register_builder(ClinicalChart, self._clinical_chart)
        self._register_builder(ClinicalChartCreate, self._clinical_chart_create)

    def _clinical_chart(self) -> ClinicalChart:
        return ClinicalChart(
            patient_id=uuid4(),
            allergies=[{"substance": "penicillin", "reaction": "rash"}],
            advance_directives="DNR on file",
            dietary_restrictions="low sodium",
            **audit_kwargs(),
        )

    def _clinical_chart_create(self, patient_id=None) -> ClinicalChartCreate:
        actor = uuid4()
        return ClinicalChartCreate(
            patient_id=patient_id or uuid4(),
            allergies=[{"substance": "latex"}],
            advance_directives="Full code",
            dietary_restrictions=None,
            created_by=actor,
        )
