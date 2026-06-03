from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.schemas.audit import AuditCreateMixin, AuditFields, AuditUpdateMixin


class _MedicationBase(BaseModel):
    name: Optional[str] = None
    dosage: Optional[str] = None
    frequency: Optional[str] = None
    route: Optional[str] = None


class MedicationCreate(_MedicationBase, AuditCreateMixin):
    name: str


class MedicationUpdate(_MedicationBase, AuditUpdateMixin):
    pass


class MedicationSearch(_MedicationBase):
    pass


class Medication(_MedicationBase, AuditFields):
    id: UUID
    name: str

    model_config = ConfigDict(from_attributes=True)
