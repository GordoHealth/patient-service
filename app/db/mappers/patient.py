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
