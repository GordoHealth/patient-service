from fastapi import FastAPI
from sqlalchemy.exc import OperationalError
from pathlib import Path

from app.services.exception_scaffold import ExceptionHandler
from app.db.exceptions import (
    DBError,
    DBLookupError,
    UnexpectedDBError,
    UniqueConstraintDBError,
    ResourceNotFoundException,
)


class AppScaffold:
    def __init__(self, dependencies: list) -> None:
        self.description = "Patient clinical data service"
        self.version = self.__get_active_branch_name()
        self.app = FastAPI(
            title="Patient Service",
            description=self.description,
            version=self.version,
            dependencies=dependencies,
            redirect_slashes=False,
            openapi_url="/openapi.json"
        )

    def create_app(self) -> FastAPI:
        self.__add_exception_handler()
        return self.app

    def __add_exception_handler(self):
        exception_handler = ExceptionHandler()
        db_error_handler = exception_handler.db_error_handler

        app = self.app
        app.add_exception_handler(
            ResourceNotFoundException, exception_handler.resource_not_found_handler
        )
        app.add_exception_handler(OperationalError, db_error_handler)
        app.add_exception_handler(DBError, db_error_handler)
        app.add_exception_handler(DBLookupError, db_error_handler)
        app.add_exception_handler(UnexpectedDBError, db_error_handler)
        app.add_exception_handler(UniqueConstraintDBError, db_error_handler)
        app.add_exception_handler(Exception, exception_handler.all_errors_handler)

    def __get_active_branch_name(self):
        head_dir = Path(".") / ".git" / "HEAD"
        with head_dir.open("r") as f:
            content = f.read().splitlines()

        for line in content:
            if line[0:4] == "ref:":
                return line.partition("refs/heads/")[2]
