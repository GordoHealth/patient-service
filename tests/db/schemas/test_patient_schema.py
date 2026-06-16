import pytest
from datetime import date
from uuid import uuid4

from pydantic import ValidationError

from app.db.models import PatientStatus
from app.schemas.care_plan import CarePlanCreate
from app.schemas.patient import PatientCreate


def test_patient_create_requires_audit_fields():
    with pytest.raises(ValidationError):
        PatientCreate(
            first_name="Jane",
            last_name="Doe",
            date_of_birth=date(1990, 1, 1),
            status=PatientStatus.active,
            mrn="MRN-001",
        )


def test_care_plan_end_date_before_start_date_raises():
    with pytest.raises(ValidationError):
        CarePlanCreate(
            patient_id=uuid4(),
            ordering_physician_id=uuid4(),
            start_date=date(2026, 3, 1),
            end_date=date(2026, 1, 1),
            created_by=uuid4(),
        )


def test_patient_create_valid():
    actor = uuid4()
    patient = PatientCreate(
        first_name="Jane",
        last_name="Doe",
        date_of_birth=date(1990, 1, 1),
        status=PatientStatus.active,
        mrn="MRN-001",
        created_by=actor,
    )
    assert patient.created_by == actor
