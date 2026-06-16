"""initial_patient_service_schema

Revision ID: a1b2c3d4e5f6
Revises:
Create Date: 2026-06-03 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "a1b2c3d4e5f6"
down_revision = None
branch_labels = None
depends_on = None

patient_status = postgresql.ENUM(
    "active",
    "discharged",
    "on_hold",
    name="patient_status",
    create_type=False,
)


def upgrade() -> None:
    patient_status.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "patients",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("first_name", sa.String(), nullable=False),
        sa.Column("last_name", sa.String(), nullable=False),
        sa.Column("date_of_birth", sa.Date(), nullable=False),
        sa.Column("status", patient_status, nullable=False),
        sa.Column("mrn", sa.String(), nullable=False),
        sa.Column("created_date", sa.DateTime(), nullable=False),
        sa.Column("last_modified_date", sa.DateTime(), nullable=False),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("last_modified_by", postgresql.UUID(as_uuid=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("index_patients_on_mrn", "patients", ["mrn"], unique=True)
    op.create_index(
        "index_patients_on_last_name_and_status",
        "patients",
        ["last_name", "status"],
        unique=False,
    )

    op.create_table(
        "medications",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("dosage", sa.Text(), nullable=True),
        sa.Column("frequency", sa.Text(), nullable=True),
        sa.Column("route", sa.Text(), nullable=True),
        sa.Column("created_date", sa.DateTime(), nullable=False),
        sa.Column("last_modified_date", sa.DateTime(), nullable=False),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("last_modified_by", postgresql.UUID(as_uuid=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "care_plans",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("patient_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("ordering_physician_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.Column("frequency_description", sa.Text(), nullable=True),
        sa.Column("created_date", sa.DateTime(), nullable=False),
        sa.Column("last_modified_date", sa.DateTime(), nullable=False),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("last_modified_by", postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(["patient_id"], ["patients.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "clinical_charts",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("patient_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("allergies", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("advance_directives", sa.Text(), nullable=True),
        sa.Column("dietary_restrictions", sa.Text(), nullable=True),
        sa.Column("created_date", sa.DateTime(), nullable=False),
        sa.Column("last_modified_date", sa.DateTime(), nullable=False),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("last_modified_by", postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(["patient_id"], ["patients.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("patient_id"),
    )

    op.create_table(
        "patient_medications",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("patient_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("medication_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.Column("is_discontinued", sa.Boolean(), nullable=False),
        sa.Column("created_date", sa.DateTime(), nullable=False),
        sa.Column("last_modified_date", sa.DateTime(), nullable=False),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("last_modified_by", postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(["patient_id"], ["patients.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["medication_id"], ["medications.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "index_patient_medications_on_patient_medication_start",
        "patient_medications",
        ["patient_id", "medication_id", "start_date"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_table("patient_medications")
    op.drop_table("clinical_charts")
    op.drop_table("care_plans")
    op.drop_table("medications")
    op.drop_table("patients")
    patient_status.drop(op.get_bind(), checkfirst=True)
