from enum import Enum
from utils.util import Util
from utils.base_model import BaseModel
from utils.db_instance import db
from utils.app_error import *


class Race(BaseModel):  # need error handling

    class Status(Enum):
        OPEN = 0
        CLOSED = 1
        LABEL = 'closed'

############################# Tried and Tested #############################
    @staticmethod
    def is_closed(race_id: dict):

        # race_id = {'race_id': N}

        race_data = Race.get_data(race_id)

        return race_data.get(Race.Status.LABEL.value) == Race.Status.CLOSED.value

# ---------------------------------------------------------------------------------
    @classmethod
    def get_races_for_event(cls, event_id: dict, filter=None):

        event_races_row_data = db.query.get_many_rows_by_att(cls, event_id)

        if not event_races_row_data:
            raise NotFoundError(
                f"No races in record for event -> {event_id}", context=AppError.get_error_context(data=event_id))

        return Util.handle_row_data(event_races_row_data)

# ---------------------------------------------------------------------------------

    @staticmethod
    def get_ticket_count(race_id: dict):
        from models.ticket import Ticket

        # race_id = {'race_id': N}
        if Race.id_exists_in_db(race_id):
            return Ticket.count_by_race(race_id)
############################# Tried and Tested #############################

    @staticmethod
    def get_horses(race_data: dict, filter=None):
        from models.horse import Horse
        if Race.id_exists_in_db(race_data):
            return Horse.get_horses_for_race(race_data)  #

    @staticmethod
    def stop_betting(race_id):

        if Race.is_closed(race_id):
            return {"error": "This race has already been closed."}

        else:

            db = get_db()
            with db:
                cursor = db.cursor()
                cursor.execute(
                    f"""
                               update {Race.TABLE} 
                               set {Race.STATUS} = ? 
                               where {Race.ID} = ? 
                               """,
                    (Race.Status.CLOSED.value, race_id),
                )

                return {"message": "Race is now closed. No more betting allowed."}
