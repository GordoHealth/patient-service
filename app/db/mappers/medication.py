from typing import Optional

from sqlalchemy import select

from app.db.mappers.base_mapper import BaseMapper
from app.db.models import Medication
from app.schemas.medication import MedicationCreate, MedicationSearch, MedicationUpdate


class MedicationMapper(
    BaseMapper[Medication, MedicationCreate, MedicationUpdate, MedicationSearch]
):
    @classmethod
    def model(cls):
        return Medication

    @classmethod
    def search_by_name(cls, name: Optional[str] = None) -> list[Medication]:
        db = cls.db()
        query = select(Medication)
        if name is not None:
            query = query.where(Medication.name.ilike(f"%{name}%"))
        return list(db.scalars(query).all())
