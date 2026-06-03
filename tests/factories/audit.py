from datetime import datetime
from uuid import UUID, uuid4


def audit_kwargs(actor_id: UUID | None = None) -> dict:
    actor = actor_id or uuid4()
    now = datetime.utcnow()
    return {
        "created_date": now,
        "last_modified_date": now,
        "created_by": actor,
        "last_modified_by": actor,
    }
