from datetime import date
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, model_validator

from app.schemas.audit import AuditCreateMixin, AuditFields, AuditUpdateMixin


class _CarePlanBase(BaseModel):
    patient_id: Optional[UUID] = None
    ordering_physician_id: Optional[UUID] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    frequency_description: Optional[str] = None

    @model_validator(mode="after")
    def validate_date_range(self):
        if self.start_date is not None and self.end_date is not None:
            if self.end_date < self.start_date:
                raise ValueError("end_date must be on or after start_date")
        return self


class CarePlanCreate(_CarePlanBase, AuditCreateMixin):
    patient_id: UUID
    ordering_physician_id: UUID
    start_date: date


class CarePlanUpdate(_CarePlanBase, AuditUpdateMixin):
    pass


class CarePlanSearch(_CarePlanBase):
    pass


class CarePlan(_CarePlanBase, AuditFields):
    id: UUID
    patient_id: UUID
    ordering_physician_id: UUID
    start_date: date

    model_config = ConfigDict(from_attributes=True)
