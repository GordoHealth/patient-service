from sqlalchemy.types import TypeDecorator
from sqlalchemy import String


class SensitiveStringType(TypeDecorator):
    """Store a string that should not be displayed."""
    impl = String
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is not None and not isinstance(value, SensitiveString):
            value = SensitiveString(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = SensitiveString(value)
        return value


class SensitiveString(str):

    def __repr__(self):
        return "****"
