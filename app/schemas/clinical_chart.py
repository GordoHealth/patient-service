from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.schemas.audit import AuditCreateMixin, AuditFields, AuditUpdateMixin


class _ClinicalChartBase(BaseModel):
    patient_id: Optional[UUID] = None
    allergies: Optional[list[Any]] = None
    advance_directives: Optional[str] = None
    dietary_restrictions: Optional[str] = None


class ClinicalChartCreate(_ClinicalChartBase, AuditCreateMixin):
    patient_id: UUID


class ClinicalChartUpdate(_ClinicalChartBase, AuditUpdateMixin):
    pass


class ClinicalChartSearch(_ClinicalChartBase):
    pass


class ClinicalChart(_ClinicalChartBase, AuditFields):
    id: UUID
    patient_id: UUID

    model_config = ConfigDict(from_attributes=True)
