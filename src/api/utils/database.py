import sqlite3
from flask import g
from pathlib import Path

DATABASE_PATH = Path("../data/raffle.db")


def get_db():
    if "db" not in g:
        # Ensure data directory exists
        DATABASE_PATH.parent.mkdir(exist_ok=True)

        g.db = sqlite3.connect(str(DATABASE_PATH))
        g.db.row_factory = sqlite3.Row

        # comment this off for debugging, it enforces relational integrity
        # comment off to insert data in the db without this constraint
        g.db.execute("PRAGMA foreign_keys = ON;")

    return g.db


def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()
