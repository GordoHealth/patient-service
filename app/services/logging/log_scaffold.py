import logging

from app.services.logging.formatted_request import FormattedRequest

logger = logging.getLogger(__name__)


class LogHandlerManager:
    def __init__(self) -> None:
        self.request = FormattedRequest()

    def set_request(self, request):
        self.request.set_request(request)

    def warn(self, message):
        logger.warning("[%s] %s\n", self.request.pretty_id, message)
