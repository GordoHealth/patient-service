import logging
import typing
from fastapi import Request
import json
from app.config.app_settings import AppSettings

logger = logging.getLogger(__name__)

HIDDEN_PARAMS_MESSAGE = "Body parameters hidden due to secure logging policy"


def format_request_id(request_id: str) -> str:
    return "\033[36m%s\033[39m" % request_id


def logging_policy():
    return AppSettings().SECURE_BODY_LOGGING


async def log_request_parameters(request: Request):
    request_id: str = request.state.request_id

    # If no request body, default to empty string
    request_body = await request.body() or ''
    if request_body:
        hidden_parameters_message = HIDDEN_PARAMS_MESSAGE
        request_body = hidden_parameters_message if logging_policy() else json.loads(request_body)

    logger.info(
        "[%s] Parameters (QUERY: %s) | (PATH: %s) | (BODY: %s)",
        format_request_id(request_id), request.query_params, request.path_params, request_body
    )


class EndpointLogFilter(logging.Filter):
    def __init__(
        self,
        path: str,
        *args: typing.Any,
        **kwargs: typing.Any,
    ):
        super().__init__(*args, **kwargs)
        self._path = path

    def filter(self, record: logging.LogRecord) -> bool:
        return record.getMessage().find(self._path) == -1


def hide_healthcheck_route_from_uvicorn_log():
    # Add filter to the logger
    logging.getLogger("uvicorn.access").addFilter(EndpointLogFilter("/health_check"))
