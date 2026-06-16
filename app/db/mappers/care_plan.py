from app.db.mappers.base_mapper import BaseMapper
from app.db.models import CarePlan
from app.schemas.care_plan import CarePlanCreate, CarePlanSearch, CarePlanUpdate


class CarePlanMapper(
    BaseMapper[CarePlan, CarePlanCreate, CarePlanUpdate, CarePlanSearch]
):
    @classmethod
    def model(cls):
        return CarePlan
