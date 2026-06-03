import logging
from datetime import datetime
from typing import TypeVar, Generic
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import select, update
from sqlalchemy.sql.expression import Update

from app.db.exceptions import db_error_manager, ResourceNotFoundException
from app.db.session import db_session
from app.db.models import Base

logger = logging.getLogger(__name__)

ModelType = TypeVar("ModelType", bound=Base)
SearchSchemaType = TypeVar("SearchSchemaType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

_AUDIT_IMMUTABLE_ON_UPDATE = frozenset({"created_date", "created_by"})


class BaseMapper(
    Generic[ModelType, CreateSchemaType, UpdateSchemaType, SearchSchemaType]
):
    @classmethod
    def get_by_id(cls, resource_id: UUID) -> ModelType:
        db = cls.db()
        model = cls.model()
        resource = db.get(model, resource_id)
        if resource is None:
            error_message = f"{model.__name__} with id {resource_id} not found"
            logger.info(error_message)
            raise ResourceNotFoundException(error_message)
        return resource

    @classmethod
    def search(cls, query_object: SearchSchemaType) -> list[ModelType]:
        model = cls.model()
        query = select(model)

        query_data = query_object.model_dump(exclude_none=True)
        for field, value in query_data.items():
            query = query.where(getattr(model, field) == value)

        db = cls.db()
        return list(db.scalars(query).all())

    @classmethod
    def _utcnow(cls) -> datetime:
        return datetime.utcnow()

    @classmethod
    def create(cls, create_object: CreateSchemaType) -> ModelType:
        db = cls.db()
        model = cls.model()
        data = create_object.model_dump()
        created_by = data["created_by"]
        now = cls._utcnow()
        data["created_date"] = now
        data["last_modified_date"] = now
        data["last_modified_by"] = created_by
        resource = model(**data)
        with db_error_manager():
            db.add(resource)
            db.commit()
            db.refresh(resource)
        return resource

    @classmethod
    def update(cls, resource_id: UUID, data: UpdateSchemaType) -> ModelType:
        db = cls.db()
        model = cls.model()
        update_data = data.model_dump(exclude_unset=True)
        last_modified_by = update_data.pop("last_modified_by")
        for field in _AUDIT_IMMUTABLE_ON_UPDATE:
            update_data.pop(field, None)
        update_data["last_modified_date"] = cls._utcnow()
        update_data["last_modified_by"] = last_modified_by
        entity_update: Update = update(model).where(model.id == resource_id)
        query = entity_update.values(**update_data)
        with db_error_manager():
            result = db.execute(query)
            db.commit()
        if result.rowcount == 0:
            error_message = f"{model.__name__} with id {resource_id} not found"
            logger.info(error_message)
            raise ResourceNotFoundException(error_message)
        resource = db.get(model, resource_id)
        return resource

    @classmethod
    def delete(cls, resource_id: UUID) -> None:
        db = cls.db()
        model = cls.model()
        resource = db.get(model, resource_id)
        if not resource:
            error_message = f"{model.__name__} with id {resource_id} not found"
            logger.info(error_message)
            raise ResourceNotFoundException(error_message)
        with db_error_manager():
            db.delete(resource)
            db.commit()

    @classmethod
    def db(cls):
        return db_session.get()

    @classmethod
    def model(cls):
        raise NotImplementedError
