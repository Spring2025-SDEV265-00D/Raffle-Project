import random
from enum import Enum
from utils.database import get_db


class Race:

    class Status(Enum):
        OPEN = (0, "OPEN")
        CLOSED = (1, "CLOSED")

        # add a label for readability
        def __new__(cls, value, label):
            obj = object.__new__(cls)
            obj._value_ = value
            obj.label = label
            return obj

    @staticmethod
    def random_least_chosen_horse(race_id):

        db = get_db()
        with db:
            cursor = db.cursor()

            # left join so horses which have not sold a ticket yet are considered
            # coalesce handle this case when ticket_count is null it makes it 0
            cursor.execute(
                """
                            select 
                             horse.id,
                             coalesce(count(ticket.horse_id), 0) as ticket_count 
                             
                             from horse 
                             left join ticket on ticket.horse_id = horse.id 
                             where horse.race_id = ? 
                             group by horse.id
                             order by ticket_count  asc
                            
            """,
                (race_id,),
            )

            roster_data = cursor.fetchall()

            if not roster_data:
                return None  # or msg?

            horse_roster = [
                {"id": horse[0], "ticket_count": horse[1]} for horse in roster_data
            ]

            # least number of times any horse was chosen
            min_count = horse_roster[0]["ticket_count"]

            # buffer is the maximum difference between least and most picked horse at any given time
            # buffer = 0 means a ticket with horse #1 will only be issue again once all horses have been issued
            # might not be desired behavior for buying several tickets

            buffer = 1
            min_count += buffer

            # grab ids of horses least chosen
            least_chosen_horses = [
                horse["id"]
                for horse in horse_roster
                if horse["ticket_count"] <= min_count
            ]

            # pick a random one to be used in ticket generation
            return random.choice(least_chosen_horses)
