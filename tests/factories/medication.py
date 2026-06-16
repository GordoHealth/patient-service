from uuid import uuid4

from faker import Faker

from app.db.models import Medication
from app.schemas.medication import MedicationCreate
from tests.factories.audit import audit_kwargs
from tests.factories.base_factory import FakerFactory


class MedicationFactory(FakerFactory):
    def __init__(self, faker_instance=None):
        super().__init__(faker_instance)
        self._register_builder(Medication, self._medication)
        self._register_builder(MedicationCreate, self._medication_create)

    def _medication(self) -> Medication:
        faker = self._faker
        return Medication(
            name=faker.word(),
            dosage="10mg",
            frequency="daily",
            route="oral",
            **audit_kwargs(),
        )

    def _medication_create(self) -> MedicationCreate:
        return MedicationCreate(
            name=self._faker.word(),
            dosage="5mg",
            frequency="BID",
            route="oral",
            created_by=uuid4(),
        )
