from fastapi import Depends

from app.api.admin.v1 import care_plans, clinical_charts, medications, patient_medications
from app.services.app_scaffold import AppScaffold
from app.logging import log_request_parameters
from app.api.admin.v1 import (
    patients,
)
from app.db.session import get_db, db_session, Session


async def set_db(db: Session = Depends(get_db)):
    db_session.set(db)


async def verify_api_key():
    """Placeholder for API key auth; overridden in tests."""
    return None


app_scaffold = AppScaffold(
    dependencies=[Depends(log_request_parameters), Depends(set_db)]
)

app = app_scaffold.create_app()
app.include_router(patients.router)
app.include_router(care_plans.router)
app.include_router(clinical_charts.router)
app.include_router(medications.router)
app.include_router(patient_medications.router)


@app.get("/")
async def root():
    return {"service": "patient-service"}
