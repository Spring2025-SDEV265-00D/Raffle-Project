from .base_meta import BaseMeta

from utils import Util, NotFoundError, DatabaseError, db


class BaseModel(metaclass=BaseMeta):

    _is_abstract = True

    @classmethod
    def add(cls, data: dict) -> dict:

        cls.check_dependency(data)

        new_model_id = None
        try:
            new_model_id = db.query.insert(cls, data)
            db.commit()

        except Exception as e:
            raise DatabaseError(
                f"Unable to add {cls.__name__}: {e}",
                context=DatabaseError.get_error_context(data=data))

        if not new_model_id:
            raise DatabaseError(
                f"Unable to add {cls.__name__}",
                context=DatabaseError.get_error_context(data=data))

        new_model_data = cls.get_data(new_model_id)
        new_model_data = Util.handle_row_data(new_model_data, cls)

        return new_model_data

    @classmethod
    def check_dependency(cls, data: dict) -> bool:
        from models import MODEL_REGISTRY
        dependency = db.query.get_foreign_keys(cls)
        if dependency is None:
            return True
        f_key = dependency['from']

        parent_class = MODEL_REGISTRY.get(f_key)

        return parent_class.id_exists_in_db(data[f_key])

    @classmethod
    def id_exists_in_db(cls, data: dict) -> bool:

        exists = db.query.has_record(cls, data)
        if not exists:
            raise NotFoundError(
                f"No record for {cls.__name__} -> {data}",
                context=NotFoundError.get_error_context(data=data))
        return exists

    @classmethod
    def get_table_name(cls):
        return cls.__name__.lower()

    @classmethod
    def get_data(cls, model_id: dict, filter=None):

        db_row = None

        if cls.id_exists_in_db(model_id):
            db_row = db.query.get_row_by_id(cls, model_id)

        if not db_row:
            raise NotFoundError(
                f"Empty records for {cls.__name__} -> {model_id}",
                context=NotFoundError.get_error_context(
                    received_data=model_id))

        return Util.handle_row_data(db_row, cls, filter)

    @classmethod
    def get_all(cls, filter=None):
        db_table_rows = db.query.get_all_from(cls)

        if not db_table_rows:
            raise NotFoundError(f"Error fetching all {cls.__name__.lower()}s",
                                context=NotFoundError.get_error_context())

        return Util.handle_row_data(db_table_rows, cls, filter)

    @classmethod
    def update_one(cls, set_clause_data: dict,
                   where_clause_data: dict) -> None:

        if not db.query.update_row_by_id(cls, set_clause_data,
                                         where_clause_data):
            raise DatabaseError(
                f"{cls.__name__} update failed -> {where_clause_data}",
                context=DatabaseError.get_error_context(
                    cls=cls,
                    set_clause_data=set_clause_data,
                    where_clause_data=where_clause_data))
