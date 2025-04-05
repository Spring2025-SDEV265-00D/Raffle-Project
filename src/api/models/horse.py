from enum import Enum
from utils.base_model import BaseModel
from utils.util import Util
from utils.db_instance import db
from utils.app_error import *


class Horse(BaseModel):

    class Status(Enum):
        ACTIVE = 0
        SCRATCHED = 1
        LABEL = 'scratched'

    ############################# Tried and Tested #############################

    # returns a list of horse_ids of horses in a race by race_id
    @staticmethod
    def get_horses_for_race(id_data: dict, filter="all") -> list:

        query_data = id_data | {
            Horse.Status.LABEL.value: Horse.Status.ACTIVE.value}
        race_roster = db.query.get_many_rows_by_att(Horse, query_data)

        if not race_roster:
            raise EmptyDataError(
                f"No horses in record for race -> {id_data}", context=AppError.get_error_context(id_data=id_data))

        horse_ids = [horse["id"] for horse in race_roster]

        return horse_ids
    ############################# Tried and Tested #############################
# ---------------------------------------------------------------------------------

    @staticmethod
    def build(data: dict) -> None:
        race_id, qtty = Util.split_dict(data)
        race_horses_count = Horse.get_count_by_att(race_id)
        new_horse_number = race_horses_count

        insert_data = []
        for _ in range(qtty['qtty']):
            new_horse_number += 1

            insert_data.append(race_id | {'horse_number': new_horse_number})

        # Util.p("horse.build", insert_data=insert_data)
        # new_horses_ids = db.query.insert_many(Horse, insert_data)
        db.query.insert_many(Horse, insert_data)


        # ---------------------------------------------------------------------------------
""" 
 try:
        x = db.query.get_count(cls, query_data)
        Util.p("x test", xTEST=x)
        return x
    except Exception as e:
        Util.p("EXCEPTION in get_count_by_att", error=str(e))
        raise """
