from utils.base_model import BaseModel
from utils.util import Util
from utils.db_instance import db
from utils.app_error import *


class Event(BaseModel):

    ############################# Tried and Tested #############################

    @staticmethod
    def get_races(data: dict, filter="all"):
        from models.race import Race
        if Event.id_exists_in_db(data):
            return Race.get_races_for_event(data, filter)

    @staticmethod
    def build_event(data: dict) -> dict:
        from sqlite3 import IntegrityError

        #        data = {
        #                'event_name' : 'Some Fair 2025',
        #                'location'    : 'Some Place',
        #                'start_date' : '2025-09-01',  #or some other format
        #                'end_date'   : '2025-09-04'
        #               }

        new_event_id = None

        try:

            new_event_id = db.query.insert(Event, data)

        except IntegrityError as e:
            raise DatabaseError(f"Unable to add event. Event names must be unique.",
                                context=AppError.get_error_context(data=data))

        if not new_event_id:
            raise DatabaseError(f"Unable to add new event.",
                                context=AppError.get_error_context(data=data))

        db.commit()
        # new_event_id = Util.id_int_to_dict(new_event_id)
        new_event_data = Event.get_data(new_event_id)
        return Util.handle_row_data(new_event_data)

    ############################# Tried and Tested #############################

    @staticmethod
    def add_races(data: dict):
        from models.race import Race
#
#   data = {'event_id'}
#
#
#
        pass
       # if Event.id_exists_in_db()
