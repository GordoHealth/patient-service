import logging
import time
import uuid

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.logging import format_request_id
from app.config.app_settings import AppSettings

logger = logging.getLogger(__name__)


class LogRequestTimeMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next) -> Response:
        if AppSettings().HIDE_HEALTHCHECK_LOGS:
            if (request.method == "GET") and (request.url.path == "/health_check"):
                response = await call_next(request)
                return response

        # Attaching UUID to each unique request
        request_uuid = str(uuid.uuid4())
        request.state.request_id = request_uuid
        formatted_request_uuid = format_request_id(request_uuid)

        logger.info("[%s] Started %s \"%s\"", formatted_request_uuid, request.method, request.url.path)

        start_time: float = time.perf_counter()
        response = await call_next(request)
        process_time: float = round((time.perf_counter() - start_time) * 1000, 2)

        logger.info("[%s] Completed %s in %sms", formatted_request_uuid, response.status_code, process_time)

        return response
