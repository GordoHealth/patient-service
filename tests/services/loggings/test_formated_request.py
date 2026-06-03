import pytest

from app.services.logging.formatted_request import FormattedRequest

from tests.utils import build_request


@pytest.fixture
def formatted_request(fastapi_request):
    formatted_request = FormattedRequest()
    formatted_request.set_request(fastapi_request)
    return formatted_request


def test_set_request_in_formatted_request(fastapi_request):
    formatted_request = FormattedRequest()
    formatted_request.set_request(fastapi_request)
    assert formatted_request.request == fastapi_request


def test_request_is_added_when_it_is_not_set():
    formatted_request = FormattedRequest()
    assert formatted_request.request is not None


def test_id_is_set_when_unset(formatted_request):
    assert formatted_request.id is not None
    assert formatted_request.id == formatted_request.request.state.request_id


def test_pretty_id_includes_request_id_and_color(formatted_request):
    pretty_id = formatted_request.pretty_id
    assert formatted_request.request.state.request_id in pretty_id
    assert "\033[36m" in pretty_id


@pytest.mark.asyncio
async def test_when_query_parameters_in_request_it_is_loaded_and_returned():
    request = build_request(query_data="test")
    formatted_request = FormattedRequest()
    formatted_request.set_request(request)
    assert formatted_request.query_params is not None
    assert str(formatted_request.query_params) == "dummyquery=test"


@pytest.mark.asyncio
async def test_when_path_parameters_in_request_it_is_loaded_and_returned():
    path_params = {"dummy": "data"}
    request = build_request(path_params=path_params)
    formatted_request = FormattedRequest()
    formatted_request.set_request(request)
    assert formatted_request.path_params is not None
    assert formatted_request.path_params == path_params
