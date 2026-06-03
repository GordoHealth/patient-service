import pytest
from pydantic import ValidationError

from app.pydantic.email import CustomEmailStr


@pytest.mark.parametrize(
    'email',
    [
        'valid@example.com',
        'example+123@example.com',
        'example.1@example.com',
        'example_123+123123@gmail.rg.net',
        'example_123+12312!!!3@gmail.rg.net'
    ]
)
def test_valid_emails(email):
    custom_email = CustomEmailStr.validate(email)
    assert custom_email == email


@pytest.mark.parametrize(
    'sensitive_email',
    [
        'valid@EXAMPLE.COM',
        'NAME@example.com'
    ]
)
def test_valid_emails_case_sensitive(sensitive_email):
    custom_email = CustomEmailStr.validate(sensitive_email)
    assert custom_email == sensitive_email


@pytest.mark.parametrize(
    'email',
    [
        '',
        '@@!!+!@!@',
        'SELECT * FROM USER;',
        'invalid',
        'example@',
        'example.com',
        'example@com',
    ]
)
def test_invalid_emails(email):
    with pytest.raises(ValueError):
        CustomEmailStr.validate(email)


@pytest.mark.parametrize(
    'email',
    [
        3,
        2.2,
        3.1459,
        True,
    ]
)
def test_invalid_type_email(email):
    with pytest.raises(ValidationError):
        CustomEmailStr.validate(email)
