from uuid import UUID

from sqlalchemy import select

from app.db.exceptions import ResourceNotFoundException
from app.db.mappers.base_mapper import BaseMapper
from app.db.models import Patient
from app.schemas.patient import PatientCreate, PatientSearch, PatientUpdate


class PatientMapper(BaseMapper[Patient, PatientCreate, PatientUpdate, PatientSearch]):
    @classmethod
    def model(cls):
        return Patient

    @classmethod
    def get_by_mrn(cls, mrn: str) -> Patient:
        db = cls.db()
        query = select(Patient).where(Patient.mrn == mrn)
        resource = db.scalars(query).first()
        if resource is None:
            raise ResourceNotFoundException(f"Patient with mrn '{mrn}' not found")
        return resource
