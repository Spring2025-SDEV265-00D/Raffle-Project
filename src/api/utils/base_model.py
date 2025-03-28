from utils.db_instance import db
from utils.util import Util
from utils.base_meta import BaseMeta


class BaseModel(metaclass=BaseMeta):

    _is_abstract = True

    @classmethod
    def get_table_name(cls):
        return cls._TABLE

    @classmethod
    def get_data(cls, query_data: dict, filter=None):

        # db_row = db.query.get_row_by_id(cls, query_data)
        db_row = db.query.get_many_rows_by_att(cls, query_data)

        if not db_row:
            return {"error": "model access"}

        return Util.handle_data(db_row, filter)

    @classmethod
    def get_all(cls, filter=None):
        db_table_rows = db.query.get_all_from(cls)

        if not db_table_rows:
            return {"error": "model access"}

        return Util.handle_data(db_table_rows, filter)

    @classmethod
    def update(cls, attribute, value):
        return

    @classmethod
    def get_count_by_att(cls, query_data: dict):
        from utils.db_instance import db

        Util.p("basemodel.get count", cls=cls, data=query_data)
        Util.f("in basemodel get count")

        x = db.query.get_count(cls, query_data)
        Util.p("x test", xTEST=x)

        return x
