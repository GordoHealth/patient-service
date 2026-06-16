from datetime import date
from uuid import uuid4

from faker import Faker

from app.db.models import Patient, PatientStatus
from app.schemas.patient import PatientCreate
from tests.factories.audit import audit_kwargs
from tests.factories.base_factory import FakerFactory


class PatientFactory(FakerFactory):
    def __init__(self, faker_instance=None):
        super().__init__(faker_instance)
        self._register_builder(Patient, self._patient)
        self._register_builder(PatientCreate, self._patient_create)

    def _patient(self) -> Patient:
        faker = self._faker
        return Patient(
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            date_of_birth=date(1970, 1, 1),
            status=PatientStatus.active,
            mrn=faker.unique.bothify(text="MRN-########"),
            **audit_kwargs(),
        )

    def _patient_create(self) -> PatientCreate:
        actor = uuid4()
        faker = self._faker
        return PatientCreate(
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            date_of_birth=date(1985, 6, 15),
            status=PatientStatus.active,
            mrn=faker.unique.bothify(text="MRN-########"),
            created_by=actor,
        )
