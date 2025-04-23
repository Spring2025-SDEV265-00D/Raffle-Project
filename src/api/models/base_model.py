from .base_meta import BaseMeta

from utils import Util
from utils import NotFoundError, DatabaseError
from utils import db


class BaseModel(metaclass=BaseMeta):

    _is_abstract = True

    @classmethod
    def id_exists_in_db(cls, data: dict) -> bool:

       # Util.f("id_exists in db BASEMODEL")
        exists = db.query.has_record(cls, data)
        if not exists:
            raise NotFoundError(
                f"No record for {cls.__name__} -> {data}", context=NotFoundError.get_error_context(data=data))
        return exists

    @classmethod
    def get_table_name(cls):
        return cls.__name__.lower()

    @classmethod
    def get_data(cls, model_id: dict, filter=None):

        db_row = None

        if cls.id_exists_in_db(model_id):
            db_row = db.query.get_row_by_id(cls, model_id)

        if not db_row:  # need t his?
            raise NotFoundError(f"Empty records for {cls.__name__} -> {model_id}",
                                context=NotFoundError.get_error_context(received_data=model_id))

        return Util.handle_row_data(db_row, cls, filter)

    @classmethod
    def get_all(cls, filter=None):
        db_table_rows = db.query.get_all_from(cls)

        if not db_table_rows:
            raise NotFoundError(
                f"Error fetching all {cls.__name__.lower()}s", context=NotFoundError.get_error_context())

        return Util.handle_row_data(db_table_rows, cls, filter)

    @classmethod
    def update_one(cls, set_clause_data: dict, where_clause_data: dict) -> None:
        # needs id_exists check if not called before// ok:ticket.cancel, stop_betting

       # Util.p("basemodel update one", whereClause=where_clause_data)

        if not db.query.update_row_by_id(cls, set_clause_data, where_clause_data):
            raise DatabaseError(
                f"{cls.__name__} update failed -> {where_clause_data}",
                context=DatabaseError.get_error_context(cls=cls,
                                                        set_clause_data=set_clause_data,
                                                        where_clause_data=where_clause_data))

    @classmethod
    def get_count_by_att(cls, query_data: dict):

        Util.p("basemodel.get count", cls=cls, data=query_data)

        count = db.query.get_count(cls, query_data)
        Util.p("x test", xTEST=count)

        return count
