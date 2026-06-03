import pytest
from pytest_mock import MockerFixture

from app import main


@pytest.fixture
def redirect_response(mocker: MockerFixture):
    mocker.patch("app.main.RedirectResponse")
    return main.RedirectResponse


@pytest.mark.asyncio
async def test_docs_redirect(redirect_response):
    docs_redirect = await main.docs_redirect()
    assert docs_redirect == redirect_response()


@pytest.mark.asyncio
async def test_redoc_redirect(redirect_response):
    redoc_redirect = await main.redoc_redirect()
    assert redoc_redirect == redirect_response()
