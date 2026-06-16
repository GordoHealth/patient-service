from fastapi import FastAPI, APIRouter, Depends, Header, HTTPException, status
from sqlalchemy import inspect

from app.db.session import get_db, db_session, Session
from app.config.app_settings import AppSettings
from app.logging import log_request_parameters


async def set_db(db: Session = Depends(get_db)):
    db_session.set(db)


async def validate_devtools_password(devtools_password: str = Header(...)):
    if devtools_password != AppSettings().DEVTOOLS_PASSWORD.get_secret_value():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unable to authenticate request",
        )


router = APIRouter(
    prefix="/devtools",
    tags=["DevTools"],
    dependencies=[
        Depends(log_request_parameters),
        Depends(set_db),
        Depends(validate_devtools_password),
    ],
)


def mount_devtools_routers(app: FastAPI) -> FastAPI:
    app.include_router(router)
    return app


@router.get(
    "/db_tables",
    response_model=list[str],
    summary="Get list of current db table names",
)
def get_db_table_list():
    db = db_session.get()
    engine = db.get_bind()
    insp = inspect(engine)
    return insp.get_table_names()
