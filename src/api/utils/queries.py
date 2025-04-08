import sqlite3
from utils.util import Util
from typing import Literal, TypedDict


class ModelDict(TypedDict):  # testing
    model_id: int | str


class QueryHelper:

    def __init__(self, connection):
        self.conn = connection  # passes the conn to obj
        self.cursor = self.conn.cursor()  # creates a cursor obj

# ---------------------------------------------------------------------------------

    def has_record(self, cls, model_id: dict | str | int) -> bool:
        table_name = cls.get_table_name()

        # Util.p("in has record", incoming=model_id)

        if isinstance(model_id, dict):
            model_id = Util.normalize_id(model_id, cls, "strip")
        else:
            model_id = Util.id_int_to_dict(model_id)
        where_clause, where_args = self.clause_builder("WHERE", model_id)
        query = f"SELECT 1 FROM {table_name} {where_clause}"

        self.cursor.execute(query, where_args)

        return self.cursor.fetchone() is not None
# ---------------------------------------------------------------------------------

    def get_printable_ticket(self, ids: list) -> list[dict]:

        _spacer = ", "
        placeholders = _spacer.join("?" for _ in ids)

        query = f"""
            SELECT
            event.event_name,
            race.race_number,
            horse.horse_number,
            ticket.id,
            created_dttm

            FROM ticket
            JOIN horse ON horse.id = ticket.horse_id
            JOIN race ON race.id = horse.race_id
            JOIN event ON event.id = race.event_id

            WHERE ticket.id IN ({placeholders})
            """

        self.cursor.execute(query, ids)

        return self.cursor.fetchall()
# ---------------------------------------------------------------------------------

    def ticket_count_for_race(self, race_id: dict) -> int:

        data = Util.normalize_id(race_id, None, "strip")
        id_value = data['id']
        # Util.f("in ticket cout race QUERY")

        query = """
            SELECT COUNT(*)
            FROM ticket t
            JOIN horse h ON t.horse_id = h.id
            WHERE h.race_id = ?"""
        args = (id_value,)

        # Util.p("inside query ticket count", query=query, args=args)

        count = self.cursor.execute(query, args).fetchone()[0]
        # dont need this, always returning (0,) if no count
        return 0 if count is None else count
# ---------------------------------------------------------------------------------

    def get_count(self, cls, query_data: dict):  # work here
        # Util.p("query.get count", cls=cls, data=query_data)
        table_name = cls.get_table_name()

        where_clause, where_args = self.clause_builder("WHERE", query_data)

        query = f"SELECT COUNT(*) FROM {table_name} {where_clause}"

        self.cursor.execute(query, where_args)

        # Util.p("in get count", countdata=self.cursor.fetchone())

        return self.cursor.fetchone()[0]
# ---------------------------------------------------------------------------------

    def get_all_from(self, cls) -> list[sqlite3.Row]:

        table_name = cls.get_table_name()
        query = f"SELECT * FROM {table_name}"
        self.cursor.execute(query)
        return self.cursor.fetchall()
# ---------------------------------------------------------------------------------

    def get_row_by_id(self, cls, model_id: dict | str | int) -> sqlite3.Row:  #

        #        if isinstance(model_id, dict):
        model_id = Util.normalize_id(model_id, cls, "strip")
#        else:
#            model_id = Util.normalize_id(model_id)

        table_name = cls.get_table_name()
        where_clause, where_args = self.clause_builder("WHERE", model_id)

        # Util.p(Util.s(), model_id=model_id)
        query = f"SELECT * FROM {table_name} {where_clause}"

        self.cursor.execute(query, where_args)

        return self.cursor.fetchone()
# ---------------------------------------------------------------------------------

    # call this Select?
    def get_many_rows_by_att(self, cls, query_data: dict) -> list[sqlite3.Row]:

        # Util.p("in get many rows QUERY", query_data=query_data)

        table_name = cls.get_table_name()

        where_clause, where_args = self.clause_builder("WHERE", query_data)

        query = f"SELECT * FROM {table_name} {where_clause}"
        args = where_args

        # Util.p("in get many rows", query=query)
        self.cursor.execute(query, args)
        # Util.p("in get many rows", data=self.cursor.fetchone())
        return self.cursor.fetchall()
# ---------------------------------------------------------------------------------

    def update_row_by_id(self, cls, set_clause_data: dict, where_clause_data: dict) -> bool:
        from utils.util import Util

        table_name = cls.get_table_name()
        where_clause_data = Util.normalize_id(where_clause_data, cls, "strip")

        # Util.p("query update row by id", cls=cls, where=where_clause_data)

        set_clause_query, set_clause_args = self.clause_builder(
            "SET", set_clause_data)

        where_clause_query, where_clause_args = self.clause_builder(
            "WHERE", where_clause_data
        )
        query = f"UPDATE {table_name} {set_clause_query} {where_clause_query}"
        args = set_clause_args + where_clause_args

       # Util.p("query.update", query=query, args=args)

        self.cursor.execute(query, args)
        self.conn.commit()  # ! need other place for this? need to commit for updates

        return self.cursor.rowcount > 0
# ---------------------------------------------------------------------------------

    def clause_builder(self, clause_type: Literal["INSERT", "WHERE", "SET"], clause_data: dict) -> tuple[str, tuple]:
        from utils.util import Util

        if not clause_data:
            return "", ()

        if clause_type == "INSERT":
            return self.insert_builder(clause_data)

        clause = f"{clause_type} "

        clause_map = {"SET": ", ", "WHERE": " AND "}

        att_spacer = clause_map.get(clause_type)

        clause_attributes = att_spacer.join(
            [f"{key} = ?" for key in clause_data])

        clause_values = tuple([clause_data[key] for key in clause_data])

        clause += clause_attributes

        return clause, clause_values

# ---------------------------------------------------------------------------------

    def insert_builder(self, clause_data: dict | list) -> tuple[str, tuple]:

        # clause_data = {"horse_idT": 1, "horseNUMM": 33}

        # Util.p("insert builder", clause_data=clause_data)

        _spacer = ", "
        clause_attributes = _spacer.join([f"{key}" for key in clause_data])
        placeholders = _spacer.join(("?") for key in clause_data)
        clause_values = tuple([clause_data[key] for key in clause_data])

        clause = f"({clause_attributes}) VALUES ({placeholders})"

        # Util.p("insert builder", query=clause)

        return clause, clause_values
# ---------------------------------------------------------------------------------

    def insert_many(self, cls, query_data: list[dict], clause_type="INSERT") -> list:

        # Util.p("insert many", query_data=query_data)

        inserted_ids_list = []

        for dictionary in query_data:
            id = self.insert(cls, dictionary, clause_type)
            inserted_ids_list.append(id)
        # attributes, args = self.clause_builder(clause_type, dictionary)
        # query = f"INSERT INTO {table_name} {attributes}"

        return inserted_ids_list
# ---------------------------------------------------------------------------------

    def insert(self, cls, query_data: dict, clause_type="INSERT") -> int:
        """_summary_
            Takes a dictionary with expected keys per class and inserts into the database.
        Returns:
            _type_: int -> Last inserted id in database. (self.cursor.lastrowid)
        """
        table_name = cls.get_table_name()

        attributes, args = self.clause_builder(clause_type, query_data)

        query = f"INSERT INTO {table_name} {attributes}"

        # Util.p("insert helper", query=query, args=args)

        self.cursor.execute(query, args)
        return self.cursor.lastrowid
