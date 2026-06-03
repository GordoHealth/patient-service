from datetime import date
from uuid import uuid4

from app.db.models import CarePlan
from app.schemas.care_plan import CarePlanCreate
from tests.factories.audit import audit_kwargs
from tests.factories.base_factory import FakerFactory


class CarePlanFactory(FakerFactory):
    def __init__(self, faker_instance=None):
        super().__init__(faker_instance)
        self._register_builder(CarePlan, self._care_plan)
        self._register_builder(CarePlanCreate, self._care_plan_create)

    def _care_plan(self) -> CarePlan:
        return CarePlan(
            patient_id=uuid4(),
            ordering_physician_id=uuid4(),
            start_date=date(2026, 1, 1),
            end_date=date(2026, 3, 1),
            frequency_description="SN 3w9",
            **audit_kwargs(),
        )

    def _care_plan_create(self, patient_id=None) -> CarePlanCreate:
        actor = uuid4()
        return CarePlanCreate(
            patient_id=patient_id or uuid4(),
            ordering_physician_id=uuid4(),
            start_date=date(2026, 1, 1),
            end_date=date(2026, 3, 1),
            frequency_description="SN 3w9",
            created_by=actor,
        )
