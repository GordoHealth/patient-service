# mypy: disable-error-code="attr-defined"

import enum
import uuid

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import as_declarative
from sqlalchemy.schema import MetaData

from app.db.session import db_session


class PatientStatus(str, enum.Enum):
    active = "active"
    discharged = "discharged"
    on_hold = "on_hold"


@as_declarative()
class Base:
    metadata = MetaData()

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    def db(self):
        return db_session.get()


class AuditMixin:
    created_date = Column(DateTime(timezone=False), nullable=False)
    last_modified_date = Column(DateTime(timezone=False), nullable=False)
    created_by = Column(UUID(as_uuid=True), nullable=False)
    last_modified_by = Column(UUID(as_uuid=True), nullable=False)


class Patient(Base, AuditMixin):
    __tablename__ = "patients"

    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    status = Column(Enum(PatientStatus, name="patient_status"), nullable=False)
    mrn = Column(String, nullable=False)

    __table_args__ = (
        Index("index_patients_on_mrn", mrn, unique=True),
        Index("index_patients_on_last_name_and_status", last_name, status),
    )


class CarePlan(Base, AuditMixin):
    __tablename__ = "care_plans"

    patient_id = Column(
        UUID(as_uuid=True),
        ForeignKey("patients.id", ondelete="CASCADE"),
        nullable=False,
    )
    ordering_physician_id = Column(UUID(as_uuid=True), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    frequency_description = Column(Text, nullable=True)


class ClinicalChart(Base, AuditMixin):
    __tablename__ = "clinical_charts"

    patient_id = Column(
        UUID(as_uuid=True),
        ForeignKey("patients.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    allergies = Column(JSONB, nullable=True)
    advance_directives = Column(Text, nullable=True)
    dietary_restrictions = Column(Text, nullable=True)


class Medication(Base, AuditMixin):
    __tablename__ = "medications"

    name = Column(Text, nullable=False)
    dosage = Column(Text, nullable=True)
    frequency = Column(Text, nullable=True)
    route = Column(Text, nullable=True)


class PatientMedication(Base, AuditMixin):
    __tablename__ = "patient_medications"

    patient_id = Column(
        UUID(as_uuid=True),
        ForeignKey("patients.id", ondelete="CASCADE"),
        nullable=False,
    )
    medication_id = Column(
        UUID(as_uuid=True),
        ForeignKey("medications.id", ondelete="CASCADE"),
        nullable=False,
    )
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    is_discontinued = Column(Boolean, nullable=False, default=False)

    __table_args__ = (
        Index(
            "index_patient_medications_on_patient_medication_start",
            patient_id,
            medication_id,
            start_date,
        ),
    )
