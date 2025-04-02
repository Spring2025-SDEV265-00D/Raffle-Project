from enum import Enum
from utils.base_model import BaseModel
from utils.util import Util
from utils.db_instance import db
from utils.app_error import *


class Horse(BaseModel):

    ############################# Tried and Tested #############################

    # returns a list of horse_ids of horses in a race by race_id
    @classmethod
    def get_horses_for_race(cls, id_data: dict, filter="all") -> list:

        race_roster = db.query.get_many_rows_by_att(cls, id_data)

        if not race_roster:
            raise EmptyDataError(
                f"No horses in record for race -> {id_data}", context=AppError.get_error_context(id_data=id_data))

        horse_ids = [horse["id"] for horse in race_roster]

        return horse_ids

    ############################# Tried and Tested #############################


""" 
 try:
        x = db.query.get_count(cls, query_data)
        Util.p("x test", xTEST=x)
        return x
    except Exception as e:
        Util.p("EXCEPTION in get_count_by_att", error=str(e))
        raise """
