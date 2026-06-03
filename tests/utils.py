import json
import uuid
from fastapi import Request
from starlette.datastructures import Headers


class CustomRequest(Request):
    async def body(self):
        return await self._body()


def build_request(
    method: str = "GET",
    server: str = "www.example.com",
    path: str = "/",
    headers: dict = {},
    body_dict: dict = {},
    state: dict = {"request_id": uuid.uuid4()},
    query_data: str = "",
    path_params={},
) -> Request:
    if headers is None:
        headers = {}
    if query_data is not None:
        formatted_query_string = f"dummyquery={query_data}"
    else:
        formatted_query_string = ""
    scope = {
        "type": "http",
        "http_version": "1.1",
        "method": method,
        "scheme": "https",
        "path": path,
        "headers": Headers(headers).raw,
        "client": ("127.0.0.1", 8080),
        "server": (server, 443),
        "state": state,
        "query_string": formatted_query_string.encode("utf-8"),
        "path_params": path_params,
    }
    if body_dict:

        async def request_body():
            return json.dumps(body_dict).encode("utf-8")

        custom_request = CustomRequest(scope, request_body)
        return custom_request
    else:
        return Request(scope=scope)
