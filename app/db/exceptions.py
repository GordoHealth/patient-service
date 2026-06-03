import contextlib
import logging
import re

import psycopg2.errors
from sqlalchemy.exc import SQLAlchemyError, DBAPIError


logger = logging.getLogger(__name__)


def _parse_unique_violation(err: psycopg2.errors.UniqueViolation):
    """parse a psycopg2 UniqueViolation error message"""
    pattern = re.compile(r"Key \((.*)\)=\((.*)\) already exists\.")
    message_detail: str
    if err.diag.message_detail:
        message_detail = err.diag.message_detail
    else:
        message_detail = ""
    match = re.search(pattern, message_detail)
    if match is None:
        error_message = f"Unexpected psycopg2 UniqueViolation message format: {err.diag.message_detail}"
        logger.error(error_message)
        raise DBError(error_message)

    table = err.diag.table_name
    (field, value) = match.groups()

    return f"({table}) already has a ({field}) with value ({value})"


@contextlib.contextmanager
def db_error_manager():
    try:
        yield
    except DBAPIError as e:
        logger.info(f"SQLAlchemy DBAPIError Exception: {e}")
        match e.orig:
            case psycopg2.errors.UniqueViolation():
                message = _parse_unique_violation(e.orig)
                raise UniqueConstraintDBError(message)
            case _:
                logger.error(f"Unexpected DB Error: {e.orig}")
                raise UnexpectedDBError(f"Unexpected DB Error: {e}")
    except SQLAlchemyError as e:
        logger.error(f"Unexpected DB Error: {e}")
        raise UnexpectedDBError(f"Unexpected DB Error: {e}")
    except LookupError as e:
        logger.error(f"Error in looking for database: {e}")
        raise DBLookupError(f"Error in looking for database: {e}")


class BaseAppException(Exception):
    """Base Exception class for all custom exceptions to inherit from. Should not be called directly."""
    pass


class DBError(BaseAppException):
    pass


class ResourceNotFoundException(BaseAppException):
    pass


class UnexpectedDBError(BaseAppException):
    pass


class UniqueConstraintDBError(BaseAppException):
    pass


class DBLookupError(BaseAppException):
    pass


class ResourceIntegrityException(Exception):
    pass
