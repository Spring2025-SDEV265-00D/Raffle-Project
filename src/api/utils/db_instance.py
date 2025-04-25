import os
from .util import Util
import sqlite3
from .database import Database, DATABASE_PATH
from werkzeug.security import generate_password_hash


DEV_MODE = True


db = Database()
# needed this to fix circular imports


def initialize_db():
    db.start_transaction()

    try:

        db.execute("PRAGMA foreign_key = ON;")

        create_tables()
        seed_role_data()
        seed_admin_data()

        if DEV_MODE:
            seed_roles_test_data()
            seed_test_data()

        db.commit()
    except:
        db.rollback()


def seed_role_data():
    from models.user import Role

    ROLES = [{'id': '1', 'description': 'Admin'},
             {'id': '2', 'description': 'Seller'},
             {'id': '3', 'description': 'Cashier'}]

    try:
        # get_all() raises an exception if table is empty
        role_table_rows = Role.get_all()

        present_ids = [str(row['role_id']) for row in role_table_rows]

        for role in ROLES:
            if role['id'] not in present_ids:
                db.query.insert(Role, role)

    except:
        db.query.insert_many(Role, ROLES)

# ?-------------------------------------------------------------------------------


def seed_admin_data():

    from models.user import User
    # from dotenv import load_dotenv
    # load_dotenv()

    admin_username = os.getenv("DEFAULT_ADMIN_USERNAME")
    admin_pw = os.getenv("DEFAULT_ADMIN_PASSWORD")
    hashed_pw = generate_password_hash(admin_pw)

    data = {'username': admin_username}
    default_admin = db.query.get_many_rows_by_att(User, data)

    if not default_admin:

        insert_data = {
            'username': admin_username,
            'password': hashed_pw,
            'role_id': '1'
        }
        db.query.insert(User, insert_data)

# ?-------------------------------------------------------------------------------


def seed_test_data():

    simulated_race = [

        """
        insert into event (event_name, location, start_date, end_date)
        values ('Lilly Fair 2022','Lafayette', '2022-01-05', '2022-01-08');
        """,
        """
        insert into race (event_id, race_number)
        values (1,1), (1,2);
        """,
        """
        insert into  horse (race_id, horse_number)
        values (1,1), (1,2), (1,3), (2,1), (2,2),(2,3);
        """,
        """
        insert into ticket (horse_id) 
        values 
        (1),(2),(3),(1),(2),(3),(1),(2),
        (4), (5), (6), (4), (5), (6), (4), (5), (6), (4), (5), (6), (4), (5);

        """
    ]
    for query in simulated_race:
        db.execute(query)

    # ?-------------------------------------------------------------------------------


def seed_roles_test_data():
    from models import User

    # create cashier and seller test users
    seller_username = {'username': 'seller'}
    cashier_username = {'username': 'cashier'}

    if not db.query.get_many_rows_by_att(User, seller_username):
        seller_data = {
            'username': 'seller',
            'password': generate_password_hash('seller123'),
            'role_id': '2'
        }
        db.query.insert(User, seller_data)

    if not db.query.get_many_rows_by_att(User, cashier_username):

        cashier_data = {
            'username': 'cashier',
            'password': generate_password_hash('cashier123'),
            'role_id': '3'
        }
        db.query.insert(User, cashier_data)

# ?-------------------------------------------------------------------------------


def create_tables():

    schema = ["""
              CREATE TABLE IF NOT EXISTS role(
                      id INTEGER PRIMARY KEY, 
                      description TEXT NOT NULL UNIQUE);

              """,
              """

              CREATE TABLE IF NOT EXISTS user(
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT NOT NULL UNIQUE,
                  password TEXT NOT NULL,
                  role_id INTEGER NOT NULL,
                  last_login_dttm TEXT,

                  FOREIGN KEY (role_id) REFERENCES role(id)
              );
              """,
              """
              CREATE TABLE IF NOT EXISTS event (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  event_name TEXT NOT NULL UNIQUE,
                  location TEXT NOT NULL,
                  start_date TEXT NOT NULL,
                  end_date TEXT NOT NULL
              );
              """,
              """
              CREATE TABLE IF NOT EXISTS race (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  event_id INTEGER NOT NULL,
                  race_number INTEGER NOT NULL CHECK (race_number > 0),
                  closed INTEGER DEFAULT 0 CHECK (closed IN (0, 1)), --Sqlite does not support boolean, we simulate it using int with a constraint

                  FOREIGN KEY (event_id) REFERENCES event(id)
              );
              """,
              """
              CREATE TABLE IF NOT EXISTS horse (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  race_id INTEGER NOT NULL,
                  horse_number INTEGER NOT NULL CHECK (horse_number > 0),
                  winner INTEGER DEFAULT 0 CHECK (winner IN (1, 0)), 
                  scratched INTEGER DEFAULT 0 CHECK (scratched IN (1, 0)), 

                  FOREIGN KEY (race_id) REFERENCES race(id)
              );
              """,
              """
              CREATE TABLE IF NOT EXISTS ticket (
                  id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  horse_id INTEGER NOT NULL,
                  created_dttm TEXT DEFAULT (datetime('now', 'localtime')),

                  
                  status INTEGER NOT NULL DEFAULT 0 CHECK (status IN (0, 1, 2)),
                  --0: "Issued/Valid"
                  --1: "Redeemed"
                  --2: "Refunded"


                  FOREIGN KEY (horse_id) REFERENCES horse(id)
              );
                  
              """]
    for query in schema:
        db.execute(query)
