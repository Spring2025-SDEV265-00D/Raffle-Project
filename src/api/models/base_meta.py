import sqlite3
from enum import Enum
from utils import DATABASE_PATH


class FieldEnumMeta(Enum):

    def __init__(self, label):
        self.label = label


class BaseMeta(type):

    def __new__(mcls, child_class_name, parent_classes, class_dict):

        # check if its BaseModel class,
        if class_dict.get("_is_abstract"):
            return super().__new__(mcls, child_class_name, parent_classes,
                                   class_dict)

        # if its one of our final models, define behavior
        # first get conn manually, to avoid using app_context from flask
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        table_name = child_class_name

        query = f"PRAGMA table_info({table_name});"
        table_column_data = cursor.execute(query).fetchall()

        # make class member holding table name
        class_dict["_TABLE"] = table_name

        # creating an enum holding the db column names for each table
        # did this to avoid hardcoding attribute column names but hasnt been helpful yet

        enum_fields = {}
        for col_data in table_column_data:
            is_pk = col_data[5] == 1
            col_name = f"{table_name.lower()}_{col_data[1]}" if is_pk else col_data[
                1]
            # col_type = col_data[2]  # not using
            enum_var_name = "ID" if is_pk else col_name.upper()
            enum_fields[enum_var_name] = (col_name)

        built_enum = FieldEnumMeta(f"{table_name}FieldEnum", enum_fields)

        class_dict["Fields"] = built_enum

        return super().__new__(mcls, child_class_name, parent_classes,
                               class_dict)
