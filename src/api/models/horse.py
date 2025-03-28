from enum import Enum
from utils.base_model import BaseModel
from utils.util import Util
from utils.db_instance import db


class Horse(BaseModel):

    # returns a list of horse_ids of horses in a race by race_id
    @classmethod
    def get_horses_for_race(cls, id_data: dict, filter="all"):

        race_roster = db.query.get_many_rows_by_att(cls, id_data)

        horse_ids = [horse["id"] for horse in race_roster]

        return horse_ids
