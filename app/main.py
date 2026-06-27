import logging.config
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.api.admin.v1.app import app as api_v1
from app.middleware import LogRequestTimeMiddleware
from app.db.logging import add_sqlalchemy_logging
from app.logging import hide_healthcheck_route_from_uvicorn_log
from app.db.healthcheck import check_database_connection
from app.config.app_settings import AppSettings
from app.config.environment import is_environment_devtools
from app.devtools.api import mount_devtools_routers


logging.config.fileConfig("logging.conf", disable_existing_loggers=False)

logger = logging.getLogger(__name__)


def add_middleware(application: FastAPI):
    # Add all middleware here

    # Logger Middleware will mimic Rails logging
    add_sqlalchemy_logging()
    application.add_middleware(LogRequestTimeMiddleware)

    app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def mount_api(application: FastAPI):
    # Mount the different versions
    application.mount("/api/admin/v1", api_v1)

    # Mount the 'latest' version
    application.mount("/api/admin/latest", api_v1)


@asynccontextmanager
async def lifespan(app: FastAPI):
    if is_environment_devtools():
        app = mount_devtools_routers(app)

    yield


app = FastAPI(
    docs_url="/devtools" if is_environment_devtools() else None,
    redoc_url=None,
    redirect_slashes=False,
    lifespan=lifespan)


add_middleware(app)
mount_api(app)

if AppSettings().HIDE_HEALTHCHECK_LOGS:
    hide_healthcheck_route_from_uvicorn_log()


@app.get(
    "/health_check",
    summary="Get response to check if service is still alive",
)
async def health_check():
    """
    Get response to check if service is still alive
    """
    return {"healthy": True}


@app.get(
    "/status",
    summary="Get database status",
)
async def status():
    """
    Get database status
    """
    return {"database": check_database_connection()}


if is_environment_devtools():
    @app.get("/", include_in_schema=False)
    @app.get("/docs", include_in_schema=False)
    async def docs_redirect():
        return RedirectResponse("/api/latest/docs")
