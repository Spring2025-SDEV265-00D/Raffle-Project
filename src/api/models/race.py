from utils.base_model import BaseModel
from utils.util import Util

# from utils.db_instance import db


class Race(BaseModel):  # need error handling

    @staticmethod
    def get_ticket_count(race_id):
        from models.ticket import Ticket

        return Ticket.get_count_by_race(race_id)

    @staticmethod
    def get_horses(race_data: dict, filter="all"):
        from models.horse import Horse

        return Horse.get_horses_for_race(race_data)
