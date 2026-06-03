from datetime import date
from uuid import uuid4

from app.db.models import PatientMedication
from app.schemas.patient_medication import PatientMedicationCreate
from tests.factories.audit import audit_kwargs
from tests.factories.base_factory import FakerFactory


class PatientMedicationFactory(FakerFactory):
    def __init__(self, faker_instance=None):
        super().__init__(faker_instance)
        self._register_builder(PatientMedication, self._patient_medication)
        self._register_builder(PatientMedicationCreate, self._patient_medication_create)

    def _patient_medication(self) -> PatientMedication:
        return PatientMedication(
            patient_id=uuid4(),
            medication_id=uuid4(),
            start_date=date(2026, 1, 1),
            end_date=None,
            is_discontinued=False,
            **audit_kwargs(),
        )

    def _patient_medication_create(
        self, patient_id=None, medication_id=None
    ) -> PatientMedicationCreate:
        return PatientMedicationCreate(
            patient_id=patient_id or uuid4(),
            medication_id=medication_id or uuid4(),
            start_date=date(2026, 1, 1),
            created_by=uuid4(),
        )
