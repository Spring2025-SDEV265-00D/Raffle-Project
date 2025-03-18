import random
from utils.database import get_db
from models.race import Race


class Event:

    @staticmethod
    def get_all_events():  # gets all events in db rn

        # get conn
        db = get_db()

        with db:

            cursor = db.cursor()

            cursor.execute("select * from event")
            event_data = cursor.fetchall()

            # make a list of dictionaries for each row
            events = [dict(event) for event in event_data]
            # print(events)

            return events

    @staticmethod
    def get_races(event_id):

        db = get_db()
        with db:
            cursor = db.cursor()
            cursor.execute(
                "select id, race_number from race where event_id = ? and closed  != ?",
                (
                    event_id,
                    Race.Status.CLOSED.value,
                ),
            )

            event_race_data = cursor.fetchall()
            event_races = [dict(race) for race in event_race_data]

            # print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            # print(event_races)
            return event_races
