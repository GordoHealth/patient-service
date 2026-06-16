from datetime import date
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.schemas.audit import AuditCreateMixin, AuditFields, AuditUpdateMixin


class _PatientMedicationBase(BaseModel):
    patient_id: Optional[UUID] = None
    medication_id: Optional[UUID] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_discontinued: Optional[bool] = None


class PatientMedicationCreate(_PatientMedicationBase, AuditCreateMixin):
    patient_id: UUID
    medication_id: UUID
    start_date: date


class PatientMedicationUpdate(_PatientMedicationBase, AuditUpdateMixin):
    pass


class PatientMedicationSearch(_PatientMedicationBase):
    pass


class PatientMedication(_PatientMedicationBase, AuditFields):
    id: UUID
    patient_id: UUID
    medication_id: UUID
    start_date: date
    is_discontinued: bool

    model_config = ConfigDict(from_attributes=True)
