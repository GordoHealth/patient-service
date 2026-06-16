import pytest
from pydantic import ValidationError
from pydantic import BaseModel

from app.pydantic.trimmed_string import TrimmedString


class Data(BaseModel):
    field: TrimmedString


def test_strimmed_string_validator():
    data = Data(field="  trimmed  ")
    assert data.field == "trimmed"

    data = Data(field="  not trimmed  ")
    assert data.field == "not trimmed"

    data = Data(field="")
    assert data.field == ""


@pytest.mark.parametrize(
    'data',
    [
        1,
        1.1,
        True,
        None
    ]
)
def test_strimmed_string_validator_with_invalid_types(data):
    with pytest.raises(ValidationError):
        Data(field=data)
