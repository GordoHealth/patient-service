from pydantic import EmailStr, TypeAdapter
from typing import Any
from pydantic_core import CoreSchema, core_schema
from pydantic import GetCoreSchemaHandler


class CustomEmailStr(str):
    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        return core_schema.no_info_after_validator_function(cls.validate, handler(str))

    @classmethod
    def validate(cls, value: str) -> str:
        #  Trimp space at the front and end of a string before regex
        if isinstance(value, str):
            value = value.strip()

        ta = TypeAdapter(EmailStr)
        ta.validate_python(value)

        return value
