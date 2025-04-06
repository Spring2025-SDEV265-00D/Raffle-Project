from enum import Enum
from utils.util import Util
from models.base_model import BaseModel
from utils.db_instance import db
from utils.app_error import *


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
                f"No races in record for event -> {event_id}", context=AppError.get_error_context(data=event_id))

        return Util.handle_row_data(event_races_row_data)

# ---------------------------------------------------------------------------------

    @staticmethod
    def get_ticket_count(race_id: dict):
        from models.ticket import Ticket

        # race_id = {'race_id': N}
        if Race.id_exists_in_db(race_id):
            return Ticket.count_by_race(race_id)
# ---------------------------------------------------------------------------------

    @staticmethod
    def get_horses(race_data: dict, filter=None):
        from models.horse import Horse
        if Race.id_exists_in_db(race_data):
            return Horse.get_horses_for_race(race_data)  #
# ---------------------------------------------------------------------------------

    @staticmethod
    def close(race_id: dict):

        # race_id = {'race_id': 3}

        if Race.is_closed(race_id):
            raise ModelStateError(
                f"Race -> {race_id} has already been closed.", context=AppError.get_error_context(race_id=race_id))

        set_data = {Race.Status.LABEL.value: Race.Status.CLOSED.value}
        Race.update_one(set_data, race_id)
        return {"message": f"Race -> {race_id} has been closed. It is no longer available for participation."}
############################# Tried and Tested #############################
# ---------------------------------------------------------------------------------

    @staticmethod
    def add_horses(data: dict):
        from models.horse import Horse
        race_id, _ = Util.split_dict(data)
        if Race.id_exists_in_db(race_id):
            return Horse.build(data)
        # ---------------------------------------------------------------------------------

    @staticmethod
    def build(data: dict) -> None:
        # from models.horse import Horse
        event_id = qtty = None
        # PROB NEEDS TRANSACTION TOO

        # incoming data
        # data = {'event_id': 3, 'qtty': 8}   qtty = 'horses_in_race'
        event_id, qtty = Util.split_dict(data)
        # Util.p("Race.build", id=event_id, qtty=qtty)

        # check how many races already in that event
        event_race_count = Race.get_count_by_att(event_id)
        new_race_number = event_race_count + 1

        insert_data = event_id.copy() | {'race_number': new_race_number}

        # Util.p("Race.build", id=event_id, qtty=qtty, insert_data=insert_data)

        # insert race_count +1 as race_num
        new_race_id = db.query.insert(Race, insert_data)
        new_race_id = Util.id_int_to_dict(new_race_id, Race)
        # Util.p("in Race.build", id=new_race_id)
       # Util.p("in Race.build", inserted_race=Race.get_data(new_race_id))

        horses_data = new_race_id.copy() | qtty

        Race.add_horses(horses_data)
        # db.commit()  # somewhere here or @caller (Event.add_race)
        pass
