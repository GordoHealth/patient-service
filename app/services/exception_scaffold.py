import traceback
from fastapi import HTTPException, status
from fastapi.exception_handlers import http_exception_handler, Request, Response
from app.db.exceptions import ResourceNotFoundException

from app.services.logging.log_scaffold import LogHandlerManager


class ExceptionHandler:
    def __init__(self) -> None:
        self._log_handler_manager = None

    @property
    def log_handler_manager(self):
        if not self._log_handler_manager:
            self._log_handler_manager = LogHandlerManager()
        return self._log_handler_manager

    async def resource_not_found_handler(self, request: Request, exc: ResourceNotFoundException) -> Response:
        self.log_handler_manager.set_request(request)
        message = traceback.format_exc()
        self.log_handler_manager.warn(message)
        self.log_handler_manager.warn(exc)
        return await http_exception_handler(
            request,
            HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(exc)
            )
        )

    async def db_error_handler(self, request: Request, exc) -> Response:
        self.log_handler_manager.set_request(request)
        message = traceback.format_exc()
        self.log_handler_manager.warn(message)
        self.log_handler_manager.warn(exc)
        return await http_exception_handler(
            request,
            HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Database Error"
            )
        )

    async def all_errors_handler(self, request: Request, exc: Exception) -> Response:
        self.log_handler_manager.set_request(request)
        message: str = traceback.format_exc()
        self.log_handler_manager.warn(message)
        self.log_handler_manager.warn(exc)
        return await http_exception_handler(
            request,
            HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal Server Error")
        )
