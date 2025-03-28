import sqlite3
from utils.util import Util


# need to handle db fails-custom exception?
# ensure not multithread with transactions, sqlite complains--done in DB class via query property


class QueryHelper:

    def __init__(self, connection):
        self.conn = connection  # passes the conn to obj
        self.cursor = self.conn.cursor()  # creates a cursor obj

    # def _build_clause(ty)

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

    def ticket_count_for_race(self, race_id: int | str) -> int:

        # Util.f("in ticket cout race QUERY")
        query = """
            SELECT COUNT(*) 
            FROM ticket t 
            JOIN horse h ON t.horse_id = h.id 
            WHERE h.race_id = ?"""
        args = (race_id,)

        # Util.p("inside query ticket count", query=query, args=args)

        count = self.cursor.execute(query, args).fetchone()[0]
        return 0 if count is None else count

    def get_all_from(self, cls):

        table_name = cls.get_table_name()
        query = f"SELECT * FROM {table_name}"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_row_by_id(self, cls, id_value):  # keep this?

        table_name = cls.get_table_name()
        id_label = cls.Fields.ID.label

        query = f"SELECT * FROM {table_name} where {id_label} = ?"
        args = (id_value,)

        self.cursor.execute(query, args)

        return self.cursor.fetchone()

    # call this Select?
    def get_many_rows_by_att(self, cls, query_data: dict):

        table_name = cls.get_table_name()

        where_clause, where_args = self.clause_builder("WHERE", query_data)

        query = f"SELECT * FROM {table_name} {where_clause}"
        args = where_args

        # Util.p("in get many rows", query=query)
        self.cursor.execute(query, args)
        return self.cursor.fetchall()

    def update(self, cls, set_clause_data: dict, where_clause_data: dict):
        from utils.util import Util

        table_name = cls.get_table_name()

        set_clause_query, set_clause_args = self.clause_builder(
            "SET", set_clause_data)

        where_clause_query, where_clause_args = self.clause_builder(
            "WHERE", where_clause_data
        )
        query = f"UPDATE {table_name} {set_clause_query} {where_clause_query}"
        args = set_clause_args + where_clause_args

        self.cursor.execute(query, args)
        # self.conn.commit()  ##########################need other place for this? need to commit for updates

        # Util.p(query, "args")
        # Util.p(args)

        return

    def clause_builder(self, clause_type, clause_data: dict):
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

    #################################################################################################################

    def insert_builder(self, clause_data: dict | list):

        # clause_data = {"horse_idT": 1, "horseNUMM": 33}

        _spacer = ", "
        clause_attributes = _spacer.join([f"{key}" for key in clause_data])
        placeholders = _spacer.join(("?") for key in clause_data)
        clause_values = tuple([clause_data[key] for key in clause_data])

        clause = f"({clause_attributes}) VALUES ({placeholders})"

        # Util.p("insert builder", query=clause)

        return clause, clause_values

    def insert_many(self, cls, query_data: list[dict], clause_type="INSERT"):
        inserted_ids_list = []

        for dictionary in query_data:
            id = self.insert(cls, dictionary, clause_type)
            inserted_ids_list.append(id)
        # attributes, args = self.clause_builder(clause_type, dictionary)
        # query = f"INSERT INTO {table_name} {attributes}"

        return inserted_ids_list

    def insert(self, cls, query_data: dict, clause_type="INSERT"):
        table_name = cls.get_table_name()

        attributes, args = self.clause_builder(clause_type, query_data)

        query = f"INSERT INTO {table_name} {attributes}"

        # Util.p("insert helper", query=query, args=args)

        self.cursor.execute(query, args)
        return self.cursor.lastrowid


"""  clause_attributes = ""
placeholders = ""
clause_values = ()

for key in clause_data:
    clause_attributes += att_spacer.join([f"{(key)}"])
    placeholders += att_spacer.join([",?"])
    clause_values + tuple(clause_data[key]) """


""" second part of insert builder for lists, dont need it anymroe
        if isinstance(clause_data, list):

            ##grab first dict and its keys // keys will be the same for all dicts
            keys = list(clause_data[0].keys())

            # Util.p("keys lista", keys=keys)

            # create a list of "?"s as long as there are keys and join them
            placeholders = _spacer.join(["?"] * len(keys))

            clause_attributes = _spacer.join(f"({key})" for key in keys)
            # Util.p("clause atts", clause_attributes=clause_attributes)

            # create a list of tuples where each touple is the value for each dict at that key
            clause_values = [
                tuple(dictionary[key] for key in keys) for dictionary in clause_data
            ]

        else: """
