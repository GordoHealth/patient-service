from typing_extensions import Annotated

from pydantic.functional_validators import AfterValidator


def trimspace(value: str) -> str:
    if isinstance(value, str):
        return value.strip()


TrimmedString = Annotated[str, AfterValidator(trimspace)]
