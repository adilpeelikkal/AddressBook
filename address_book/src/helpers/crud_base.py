from typing import Optional, Type, TypeVar, Union, Any

from sqlalchemy.orm import Session
from sqlalchemy import select, delete

from src.db.base_class import Base

from pydantic import BaseModel
from src.schemas.pagination import SkipLimit


ModelType = TypeVar("ModelType", bound=Base)
InDBSchemaType = TypeVar("InDBSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CrudBase:
    """
    Generic CRUD operations for SQLAlchemy models.
    """

    def __init__(self, table_model: Type[ModelType]) -> None:
        """
        Initializes the CrudBase with the SQLAlchemy model to operate on.

        Args:
            table_model (Type[ModelType]): SQLAlchemy model to perform CRUD operations on.
        """
        self.table_model = table_model

    def get(self, session: Session, query_filter=None) -> Union[Optional[ModelType]]:
        """
        Retrieves a single record from the database based on the provided filter.
        """
        query = select(self.table_model)
        if query_filter is not None:
            query = query.filter(query_filter)
        result = session.execute(query)
        return result.scalars().first()

    def get_multi(
        self,
        session: Session,
        query_filter=None,
        skip: Optional[SkipLimit] = None,
    ) -> list[ModelType]:
        """
        Retrieves multiple records from the database based on the provided filter
        and pagination parameters.
        """
        query = select(self.table_model)
        if query_filter is not None:
            query = query.filter(query_filter)
        if skip:
            query = query.offset((skip.page - 1) * skip.limit).limit(skip.limit)

        result = session.execute(query)
        return result.scalars().all()

    def create(self, session: Session, *, obj_to_create: InDBSchemaType) -> ModelType:
        """
        Creates a new record in the database.
        """

        db_obj: ModelType = self.table_model(**obj_to_create.model_dump())
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj

    def update(
        self,
        session: Session,
        updated_obj: UpdateSchemaType,
        db_obj_to_update: ModelType,
    ) -> Optional[ModelType]:
        """
        Updates an existing record in the database.
        """
        if db_obj_to_update:
            existing_obj_to_update_data = db_obj_to_update.__dict__
            updated_data: dict[str, Any] = updated_obj.model_dump()
            for field in existing_obj_to_update_data:
                if field in updated_data:
                    setattr(db_obj_to_update, field, updated_data[field])
            session.add(db_obj_to_update)
            session.commit()
            session.refresh(db_obj_to_update)
        return db_obj_to_update

    def delete(self, session: Session, id_to_delete: int) -> None:
        """
        Deletes a record from the database.
        """
        query = delete(self.table_model).where(self.table_model.id == id_to_delete)
        session.execute(query)
        session.commit()
