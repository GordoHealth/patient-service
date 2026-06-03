from app.db.exceptions import ResourceNotFoundException
from app.db.mappers.base_mapper import BaseMapper
from app.db.mappers.medication import MedicationMapper
from app.db.mappers.patient import PatientMapper
from app.db.models import PatientMedication
from app.schemas.patient_medication import (
    PatientMedicationCreate,
    PatientMedicationSearch,
    PatientMedicationUpdate,
)


class PatientMedicationMapper(
    BaseMapper[
        PatientMedication,
        PatientMedicationCreate,
        PatientMedicationUpdate,
        PatientMedicationSearch,
    ]
):
    @classmethod
    def model(cls):
        return PatientMedication

    @classmethod
    def create(cls, create_object: PatientMedicationCreate) -> PatientMedication:
        try:
            PatientMapper.get_by_id(create_object.patient_id)
        except ResourceNotFoundException as exc:
            raise ResourceNotFoundException(
                f"Patient with id {create_object.patient_id} not found"
            ) from exc
        try:
            MedicationMapper.get_by_id(create_object.medication_id)
        except ResourceNotFoundException as exc:
            raise ResourceNotFoundException(
                f"Medication with id {create_object.medication_id} not found"
            ) from exc
        return super().create(create_object)
