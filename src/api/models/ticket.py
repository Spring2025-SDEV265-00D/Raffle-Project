from utils.util import Util

from utils.db_instance import db
from utils.base_model import BaseModel


class Ticket(BaseModel):

    @classmethod
    def batching(cls, batch_data: list[dict]) -> list[dict]:

        prepared_order = None

        db.start_transaction()
        try:

            prepared_order = Ticket.handle_order(batch_data)
            db.commit()

        except:
            db.rollback()
            raise  # yet to define AppError

        return prepared_order

    @staticmethod
    def get_count_by_race(race_id: int | str):

        return db.query.ticket_count_for_race(race_id)

    @classmethod
    def handle_order(cls, data: list[dict]) -> list[dict]:
        from models.race import Race

        # data= [{"race_id": "1", "qtty": 1}, {"race_id": "2", "qtty": 2}]

        new_ticket_ids = []

        for dictionary in data:

            # to be passed to Race.get_horses(dict)
            # uses a generic query function that expects a dict
            get_horses_data = {"race_id": dictionary["race_id"]}

            race_id = dictionary["race_id"]
            qtty = dictionary["qtty"]

            horses_in_race = Race.get_horses(get_horses_data)

            ticket_count = Ticket.get_count_by_race(race_id)
            query_data = Util.round_robin_pick(
                horses_in_race, ticket_count, qtty)
            tickets_for_this_race = db.query.insert_many(cls, query_data)

            new_ticket_ids.extend(tickets_for_this_race)

        order_rows = db.query.get_printable_ticket(new_ticket_ids)
        return Util.handle_data(order_rows)
