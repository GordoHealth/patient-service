from datetime import date, datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.db.models import PatientStatus
from app.pydantic.trimmed_string import TrimmedString
from app.schemas.audit import AuditCreateMixin, AuditFields, AuditUpdateMixin


class _PatientBase(BaseModel):
    first_name: Optional[TrimmedString] = None
    last_name: Optional[TrimmedString] = None
    date_of_birth: Optional[date] = None
    status: Optional[PatientStatus] = None
    mrn: Optional[TrimmedString] = None


class PatientCreate(_PatientBase, AuditCreateMixin):
    first_name: TrimmedString
    last_name: TrimmedString
    date_of_birth: date
    status: PatientStatus
    mrn: TrimmedString


class PatientUpdate(_PatientBase, AuditUpdateMixin):
    pass


class PatientSearch(_PatientBase):
    pass


class Patient(_PatientBase, AuditFields):
    id: UUID
    first_name: TrimmedString
    last_name: TrimmedString
    date_of_birth: date
    status: PatientStatus
    mrn: TrimmedString

    model_config = ConfigDict(from_attributes=True)
