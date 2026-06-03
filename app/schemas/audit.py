from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class AuditFields(BaseModel):
    created_date: datetime
    last_modified_date: datetime
    created_by: UUID
    last_modified_by: UUID

    model_config = ConfigDict(from_attributes=True)


class AuditCreateMixin(BaseModel):
    created_by: UUID


class AuditUpdateMixin(BaseModel):
    last_modified_by: UUID
