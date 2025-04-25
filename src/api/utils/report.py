from .db_instance import db
from .util import Util


class Report():

    @staticmethod
    def by_race(race_id: dict):

        report = []

        from models import Horse
        horses_rows_in_race = db.query.get_many_rows_by_att(Horse, race_id)
        roster: list = Util.handle_row_data(horses_rows_in_race, Horse)

        from models import Ticket
        for horse in roster:
            horse_id = {'horse_id': horse['horse_id']}
            ticket_count = db.query.get_count(Ticket, horse_id)
            horse.pop('horse_id', None)
            horse.pop('race_id', None)
            horse['tickets_sold'] = ticket_count
           # print(horse)
            report.append(horse)

        return report
