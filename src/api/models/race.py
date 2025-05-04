from enum import Enum
from .base_model import BaseModel
from utils import Util, NotFoundError, ModelStateError, db


class Race(BaseModel):  # need error handling

    class Status(Enum):
        OPEN = 0
        CLOSED = 1
        LABEL = 'closed'

    @staticmethod
    def update(request_data: dict) -> dict:
        response = None
        horse_id, request_type = Util.split_dict(request_data)
        request_type = request_type['request']

        from .horse import Horse
        race_id = Horse.get_data(horse_id, 'race_id')

        # request_type = {'winner'}
        if request_type == 'winner':
            if not Race.is_closed(race_id):
                raise ModelStateError(
                    "Unable to set winner. Race is not closed",
                    context=ModelStateError.get_error_context(
                        request_data=request_data))

            response = Horse.set_winner(horse_id)

        elif request_type == 'scratched':
            response = Horse.set_scratched(horse_id)

        else:
            raise ModelStateError(f"Invalid request type -> {request_type}.",
                                  context=ModelStateError.get_error_context(
                                      request_data=request_data))
            # not sure if scratching can be done after race is closed
            # (disqualified horse?) leaving it possible for now

        return response

    @staticmethod
    def is_closed(race_id: dict):
        race_data = Race.get_data(race_id)
        return race_data.get(
            Race.Status.LABEL.value) == Race.Status.CLOSED.value

    @classmethod
    def get_races_for_event(cls, event_id: dict, filter=None):
        event_races_row_data = db.query.get_many_rows_by_att(cls, event_id)

        if not event_races_row_data:
            raise NotFoundError(
                f"No races in record for event -> {event_id}",
                context=NotFoundError.get_error_context(data=event_id))

        return Util.handle_row_data(event_races_row_data, Race)

    @staticmethod
    def get_ticket_count(race_id: dict):
        from .ticket import Ticket

        if Race.id_exists_in_db(race_id):
            return Ticket.count_by_race(race_id)

    @staticmethod
    def get_horses(race_data: dict, filter=None):
        from .horse import Horse
        if Race.id_exists_in_db(race_data):
            return Horse.get_horses_for_race(race_data, filter)  #

    @staticmethod
    def close(race_id: dict):

        if Race.is_closed(race_id):
            raise ModelStateError(
                f"Race -> {race_id} has already been closed.",
                context=ModelStateError.get_error_context(race_id=race_id))

        set_data = {Race.Status.LABEL.value: Race.Status.CLOSED.value}
        Race.update_one(set_data, race_id)
        return {
            "message":
            f"Race -> {race_id} has been closed. It is no longer available for participation."
        }
