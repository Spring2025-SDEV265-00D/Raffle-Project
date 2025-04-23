from enum import Enum

from .base_model import BaseModel

from utils import Util
from utils import db
from utils import ModelStateError


class Ticket(BaseModel):

    class Status(Enum):
        ACTIVE = 0  # Default status
        REDEEM = 1  # Once a winning ticket is paid out

        # Once a refund has been issued. (Horse scratched after ticket sales have begun)
        REFUND = 2
        LABEL = 'status'

    ############################# Tried and Tested #############################

    @staticmethod
    def count_by_race(race_id: dict):
        sold_tickets = db.query.ticket_count_for_race(race_id)

        # sqlite returns either 0 (no tickets) or [] empty list (no race_id match)
        # Race checks for race_id validity

#        if not sold_tickets:
#            raise EmptyDataError(
#                f"No tickets sold for race -> {race_id}", context=AppError.get_error_context(race_id=race_id))
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
        from .race import Race

        # listOfDicts = [{"race_id": "1", "qtty": 1}, {"race_id": "2", "qtty": 2}]

        new_ticket_ids = []

        for order_line in order_data:

            # Util.p("ticket handlw order", items=order_line.items())

            race_id_data = {"race_id": order_line["race_id"]}
            qtty = order_line["qtty"]

            # this function also checks if race_id exists in fact, and throws error if not
            if Race.is_closed(race_id_data):
                raise ModelStateError(
                    f"Race -> {race_id_data} is closed. Cannot sell tickets.")

            horses_in_race = Race.get_horses(race_id_data, 'id')
            # Util.p('ticket handle order', horses_in_race=horses_in_race)

            ticket_count = Race.get_ticket_count(race_id_data)

            query_data = Util.round_robin_pick(
                horses_in_race, ticket_count, qtty)

            tickets_for_this_race = db.query.insert_many(Ticket, query_data)

            new_ticket_ids.extend(tickets_for_this_race)

        order_rows = db.query.get_printable_ticket(new_ticket_ids)
        return Util.handle_row_data(order_rows, Ticket)
# ---------------------------------------------------------------------------------

    #!deprecated, replaced by update_standing

    @staticmethod
    def cancel(ticket_id: dict):
        LABEL = Ticket.Status.LABEL.value
        ticket_data = Ticket.get_data(ticket_id)

        ticket_status = Ticket.Status(ticket_data[LABEL])

        if ticket_status in (Ticket.Status.REFUND, Ticket.Status.REDEEM):
            raise ModelStateError(
                f"Ticket -> {ticket_id} was already {ticket_status.name.lower()}.", context=AppError.get_error_context(ticket_id=ticket_id))

        set_data = {LABEL: Ticket.Status.REFUND.value}

        Ticket.update_one(set_data, ticket_id)
        return {"message": f"Ticket -> {ticket_id} has been marked as {Ticket.Status.REFUND.name.lower()}."}

    ############################# Tried and Tested #############################

    @staticmethod
    def update_standing(request_data: dict) -> dict:
        LABEL = Ticket.Status.LABEL.value
        ticket_id, request_type = Util.split_dict(request_data)

        ticket_data = Ticket.get_data(ticket_id)
        ticket_status = Ticket.Status(ticket_data['status'])

        id: str = 'horse_id'
        horse_id = {id: ticket_data[id]}

        request_type = request_type['request'].upper()

        if ticket_status in (Ticket.Status.REFUND, Ticket.Status.REDEEM):
            raise ModelStateError(f"Ticket -> {ticket_id} has already been {ticket_status.name.lower()}ed.",
                                  context=ModelStateError.get_error_context(request_data=request_data))

        if request_type not in (Ticket.Status.REDEEM.name, Ticket.Status.REFUND.name):
            raise ModelStateError(
                f"Invalid request type -> {request_type}.", context=ModelStateError.get_error_context(request_data=request_data))

        set_data = {}
        # {'request': 'redeem' or 'refund'}
        if request_type == Ticket.Status.REDEEM.name:
            # check if tik is winner

            if Ticket._is_redeemable(horse_id):
                set_data = {LABEL: Ticket.Status.REDEEM.value}

        elif request_type == Ticket.Status.REFUND.name:

            if Ticket._is_refundable(horse_id):
                set_data = {LABEL: Ticket.Status.REFUND.value}

        if not set_data:
            raise ModelStateError(
                f"Invalid operation -> Ticket {ticket_id} is not {request_type.lower()}able.", context=ModelStateError.get_error_context(
                    request_data=request_data))

        Ticket.update_one(set_data, ticket_id)

        return {"message": f"Ticket -> {ticket_id} has been {request_type.lower()}ed"}

    @staticmethod
    def _is_redeemable(horse_id: dict) -> bool:
        from .horse import Horse
        return Horse.is_winner(horse_id)

    @staticmethod
    def _is_refundable(horse_id: dict) -> bool:
        from .horse import Horse
        return Horse.is_scratched(horse_id)
