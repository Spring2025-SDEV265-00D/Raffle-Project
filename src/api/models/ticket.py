from utils.util import Util

from utils.db_instance import db
from utils.base_model import BaseModel
from utils.app_error import *
from enum import Enum


class Ticket(BaseModel):

    class Status(Enum):
        ACTIVE = 0
        REDEEMED = 1
        CANCELED = 2
        LABEL = 'status'

    ############################# Tried and Tested #############################
    @staticmethod
    def count_by_race(race_id: dict):
        sold_tickets = db.query.ticket_count_for_race(race_id)

        # sqlite returns either 0 (no tickets) or [] empty list (no race_id match)
        # Race checks for race_id validity

        if not sold_tickets:
            raise EmptyDataError(
                f"No tickets sold for race -> {race_id}", context=AppError.get_error_context(race_id=race_id))
        return sold_tickets
# ---------------------------------------------------------------------------------

#    @classmethod
    @staticmethod
    def batching(batch_data: list[dict]) -> list[dict]:

        prepared_order = None

        db.start_transaction()
        try:

            prepared_order = Ticket.handle_order(batch_data)
            db.commit()

        except:
            db.rollback()
            raise  # raises back whatever was raised below

        return prepared_order
# ---------------------------------------------------------------------------------

   # @classmethod
    @staticmethod
    def handle_order(order_data: list[dict]) -> list[dict]:
        from models.race import Race

        # listOfDicts = [{"race_id": "1", "qtty": 1}, {"race_id": "2", "qtty": 2}]

        new_ticket_ids = []

        for order_line in order_data:

            # Util.p("ticket handlw order", items=order_line.items())

            race_id_data = {"race_id": order_line["race_id"]}
            qtty = order_line["qtty"]

            horses_in_race = Race.get_horses(race_id_data)
            # Util.p('ticket handle order', horses_in_race=horses_in_race)

            ticket_count = Race.get_ticket_count(race_id_data)

            query_data = Util.round_robin_pick(
                horses_in_race, ticket_count, qtty)
            tickets_for_this_race = db.query.insert_many(Ticket, query_data)

            new_ticket_ids.extend(tickets_for_this_race)

        order_rows = db.query.get_printable_ticket(new_ticket_ids)
        return Util.handle_row_data(order_rows)

    @staticmethod
    def cancel(ticket_id: dict):
        LABEL = Ticket.Status.LABEL.value
        ticket_data = Ticket.get_data(ticket_id)

        ticket_status = Ticket.Status(ticket_data[LABEL])

        if ticket_status in (Ticket.Status.CANCELED, Ticket.Status.REDEEMED):
            raise ModelStateError(
                f"Ticket -> {ticket_id} was already {ticket_status.name.lower()}.", context=AppError.get_error_context(ticket_id=ticket_id))

        set_data = {LABEL: Ticket.Status.CANCELED.value}

        Ticket.update_one(set_data, ticket_id)
        return {"message": f"Ticket -> {ticket_id} has been canceled."}

    ############################# Tried and Tested #############################
