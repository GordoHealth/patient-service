from dataclasses import dataclass
from enum import Enum
from typing import Optional

from sqlalchemy import text

from app.db.session import engine


class DBStatus(str, Enum):
    UP = "UP"
    DOWN = "DOWN"
    UNKNOWN = "UNKNOWN"


@dataclass
class DBHealthDetails:
    engine: Optional[str] = None
    failure: Optional[str] = None


@dataclass
class DBHealthStatus:
    status: DBStatus
    details: DBHealthDetails


def check_database_connection():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            if result.scalar() == 1:
                return DBHealthStatus(status=DBStatus.UP, details=DBHealthDetails(engine.name))
        return DBHealthStatus(status=DBStatus.UNKNOWN, details=DBHealthDetails(engine.name, 'Can NOT ping to database'))
    except Exception as e:
        return DBHealthStatus(status=DBStatus.DOWN, details=DBHealthDetails(engine.name, str(e)))
