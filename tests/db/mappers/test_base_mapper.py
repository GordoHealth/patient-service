from app.db.mappers.patient import PatientMapper
from app.db.models import Patient


def test_patient_mapper_model():
    assert PatientMapper.model() is Patient
