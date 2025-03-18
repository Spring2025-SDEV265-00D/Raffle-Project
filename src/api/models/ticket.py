import random
from enum import Enum
from utils.database import get_db
from models.race import Race


class Ticket:

    class Status(Enum):
        ACTIVE = (0, "ACTIVE")
        REDEEMED = (1, "REDEEMED")
        CANCELED = (2, "CANCELED")

        # add a label for readability
        def __new__(cls, value, label):
            obj = object.__new__(cls)
            obj._value_ = value
            obj.label = label
            return obj

    def __init__(self, reference_number=None, race_id=None, horse_id=None):
        self.reference_number = reference_number
        self.race_id = race_id
        self.horse_id = horse_id

    # returns all ticket data relevant to the customer
    @staticmethod
    def get_ticket_data(reference_number):

        db = get_db()
        with db:
            cursor = db.cursor()
            cursor.execute(
                """select 
                    event.event_name, 
                    race.race_number, 
                    horse.horse_number,
                    ticket.reference_number,
                    ticket.created_dttm 
                    
                    from ticket
                    join horse on horse.id = ticket.horse_id
                    join race on race.id = horse.race_id
                    join event on event.id = race.event_id
                    where ticket.reference_number = ?
                """,
                (reference_number,),
            )

            ticket_row = cursor.fetchone()
            ticket_data = dict(ticket_row)

        # print(ticket_data)

        return ticket_data

    @staticmethod
    def create_ticket(race_id):
        db = get_db()  # getting connection

        with db:
            cursor = db.cursor()

            horse_id = Race.random_least_chosen_horse(race_id)

            cursor.execute("INSERT INTO ticket (horse_id) VALUES (?)", (horse_id,))

            reference_number = cursor.lastrowid

            return Ticket.get_ticket_data(reference_number)

    @staticmethod
    def get_status(reference_number):

        db = get_db()

        with db:
            cursor = db.cursor()

            # check ticket status
            cursor.execute(
                "select status_code from ticket where reference_number = ?",
                (reference_number,),
            )  # needs to be a tuple to use ?
            current_status = cursor.fetchone()  # grabbing row

            if current_status is None:  # if ticket # doesnt exist
                return {"error": "Ticket not found"}

            return {"status": Ticket.Status(current_status[0]).label}

    @staticmethod
    def cancel_ticket(reference_number):

        status_data = Ticket.get_status(reference_number)

        # if error msg, return it
        if status_data.get("error"):
            return status_data

        status = status_data.get("status")

        if status == Ticket.Status.ACTIVE.label:

            db = get_db()

            with db:
                cursor = db.cursor()
                cursor.execute(
                    "update ticket set status_code = ? where reference_number =?",
                    (Ticket.Status.CANCELED.value, reference_number),
                )

        response = {
            Ticket.Status.CANCELED.label: {
                "message": "Ticket #"
                + str(reference_number)
                + " has already been canceled."
            },
            Ticket.Status.REDEEMED.label: {
                "message": "Ticket #"
                + str(reference_number)
                + " has already been redeemed."
            },
            Ticket.Status.ACTIVE.label: {
                "message": "Ticket #" + str(reference_number) + " is now canceled."
            },
        }

        return response.get(status)
