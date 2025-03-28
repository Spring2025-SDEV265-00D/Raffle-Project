import sqlite3
from flask import g
from pathlib import Path
from utils.queries import QueryHelper

DATABASE_PATH = Path("../data/raffle.db")


class Database:

    def __init__(self):
        # make sure directory exists
        DATABASE_PATH.parent.mkdir(exist_ok=True)
        self._query = None

    def get_conn(self):

        if "db" not in g:

            g.db = sqlite3.connect(str(DATABASE_PATH))
            g.db.row_factory = sqlite3.Row  # allow data retrieval as dicts

            # comment this off for debugging, it enforces relational integrity
            # comment off to insert data in the db without this constraint
        #      g.db.execute("PRAGMA foreign_keys = ON;")

        return g.db

    def close_conn(self, e=None):
        db = g.pop("db", None)
        if db is not None:
            db.close()

    def start_transaction(self):
        self.get_conn().execute("BEGIN")

    def commit(self):
        self.get_conn().commit()

    def rollback(self):
        self.get_conn().rollback()

    # using this to get the query helper and get us the raw SQL
    @property
    def query(self):
        if "query_helper" not in g:
            g.query_helper = QueryHelper(self.get_conn())
        return g.query_helper
