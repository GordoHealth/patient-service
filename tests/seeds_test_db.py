from app.db import models
from tests.factories.patient import PatientFactory
from tests.conftest import insert_to_db


def seed_test_db(init_test_db):
    patient = PatientFactory().create(models.Patient)
    insert_to_db(patient)
