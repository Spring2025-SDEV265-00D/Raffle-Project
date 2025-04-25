from enum import Enum

from .base_model import BaseModel

from utils import Util
from utils import NotFoundError, ModelStateError
from utils import db


class Race(BaseModel):  # need error handling

   # ID = 'race_id'

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
                f"No races in record for event -> {event_id}", context=NotFoundError.get_error_context(data=event_id))

        return Util.handle_row_data(event_races_row_data, Race)

# ---------------------------------------------------------------------------------

    @staticmethod
    def get_ticket_count(race_id: dict):
        from .ticket import Ticket

        # race_id = {'race_id': N}
        if Race.id_exists_in_db(race_id):
            return Ticket.count_by_race(race_id)
# ---------------------------------------------------------------------------------

    @staticmethod
    def get_horses(race_data: dict, filter=None):
        from .horse import Horse
        if Race.id_exists_in_db(race_data):
            return Horse.get_horses_for_race(race_data, filter)  #
# ---------------------------------------------------------------------------------

    @staticmethod
    def close(race_id: dict):

        # race_id = {'race_id': 3}

        if Race.is_closed(race_id):
            raise ModelStateError(
                f"Race -> {race_id} has already been closed.", context=ModelStateError.get_error_context(race_id=race_id))

        set_data = {Race.Status.LABEL.value: Race.Status.CLOSED.value}
        Race.update_one(set_data, race_id)
        return {"message": f"Race -> {race_id} has been closed. It is no longer available for participation."}
