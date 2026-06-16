from typing import Optional
from fastapi import Request
from starlette.datastructures import QueryParams


class FormattedRequest:
    _instance = None

    def __init__(self) -> None:
        self._request: Optional[Request] = None
        self._id: Optional[str] = None
        self._query_params: Optional[QueryParams] = None
        self._path_params: Optional[dict] = None

    def set_request(self, request):
        self._request = request

    @property
    def request(self) -> Request:
        if self._request is None:
            self._request = Request({"type": "http"})
        return self._request

    @property
    def id(self) -> str:
        if self._id is None:
            self._id = self.request.state.request_id
        return self._id

    @property
    def pretty_id(self) -> str:
        return "\033[36m%s\033[39m" % self.id

    @property
    def query_params(self) -> QueryParams:
        if self._query_params is None:
            self._query_params = self.request.query_params
        return self._query_params

    @property
    def path_params(self) -> dict:
        if self._path_params is None:
            self._path_params = self.request.path_params
        return self._path_params
