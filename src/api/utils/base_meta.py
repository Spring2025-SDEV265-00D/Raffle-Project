from enum import Enum
from types import SimpleNamespace
from utils.db_instance import db
from utils.database import DATABASE_PATH
import sqlite3
from utils.util import Util


class FieldEnumMeta(Enum):
    def __init__(self, label, full_name):
        self.label = label
        self.full_name = full_name


class BaseMeta(type):
    def __new__(mcls, child_class_name, parent_classes, class_dict):

        # check if its BaseModel class,
        if class_dict.get("_is_abstract"):
            return super().__new__(mcls, child_class_name, parent_classes, class_dict)

        # if its one of our final models, define behavior
        # first get conn manually, to avoid using app_context from flask
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        table_name = child_class_name

        query = f"PRAGMA table_info({table_name});"
        table_column_data = cursor.execute(query).fetchall()

        # make class member holding table name
        class_dict["_TABLE"] = table_name

        enum_fields = {}
        for col_data in table_column_data:
            col_name = col_data[1]
            col_type = col_data[2]  # not using
            is_pk = col_data[5] == 1

            enum_var_name = "ID" if is_pk else col_name.upper()
            full_name = f"{table_name}.{col_name}"

            # Util.p(col_name)

            enum_fields[enum_var_name] = (col_name, full_name)

        built_enum = FieldEnumMeta(f"{table_name}FieldEnum", enum_fields)

        class_dict["Fields"] = built_enum

        #        t = class_dict["Fields"]
        #        if table_name == "Event":
        #            for name, fullName in t.__members__.items():
        #                Util.p("class dict", name=name, data=fullName)
        # if child_class_name == "Event":

        return super().__new__(mcls, child_class_name, parent_classes, class_dict)


# puts all db atts in a dictionary, not super useful
""" 
    def __new__(mcls, child_class_name, parent_classes, class_dict):

        # check if its BaseModel class,
        if class_dict.get("_is_abstract"):
            return super().__new__(mcls, child_class_name, parent_classes, class_dict)

        # if its one of our final models, define behavior
        # first get conn manually, to avoid using app_context from flask
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        query = f"PRAGMA table_info({child_class_name});"
        table_column_data = cursor.execute(query).fetchall()

        # now populate class dictionary with desired variables
        # all column names from db are stored in a dictionary called _FIELDS in the format:{TABLE.COLUMN : column} 'RACE.EVENT_ID': 'event_id'

        class_dict["_TABLE"] = child_class_name
        class_dict["_FIELDS"] = {}

        for col_data in table_column_data:
            col_name = col_data[1]
            col_type = col_data[2]  # not using this right now...

            key = f"{child_class_name}.{col_name}".upper()

            class_dict["_FIELDS"][key] = col_name

        if child_class_name == "Event":
            Util.p("class dict", dic=class_dict["_FIELDS"])

        return super().__new__(mcls, child_class_name, parent_classes, class_dict)
 """
