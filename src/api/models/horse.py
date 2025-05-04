from enum import Enum
from .base_model import BaseModel
from utils import Util, EmptyDataError, ModelStateError, db


class Horse(BaseModel):
    WINNER = 1

    class Status(Enum):
        ACTIVE = 0
        SCRATCHED = 1
        LABEL = 'scratched'

    @staticmethod
    def get_horses_for_race(id_data: dict,
                            filter: list[str] | str = None) -> list:

        query_data = id_data | {
            Horse.Status.LABEL.value: Horse.Status.ACTIVE.value
        }
        race_roster = db.query.get_many_rows_by_att(Horse, query_data)

        if not race_roster:
            raise EmptyDataError(
                f"No horses in record for race -> {id_data}",
                context=EmptyDataError.get_error_context(id_data=id_data))

        return Util.handle_row_data(race_roster, Horse, filter)

    @staticmethod
    def set_winner(horse_id: dict) -> dict:

        winner_data = {'winner': Horse.WINNER}
        race_id = Horse.get_data(horse_id, 'race_id')
        query_data = race_id | winner_data

        # get context to avoid repeating
        context = ModelStateError.get_error_context(query_data=query_data,
                                                    horse_id=horse_id)

        if Horse.is_scratched(horse_id):
            raise ModelStateError(
                "This horse is marked as scratched, cannot mark it as winner",
                context=context)

        elif Horse.is_winner(horse_id):
            raise ModelStateError("This horse is already marked as a winner.",
                                  context=context)

        # need to check if theres already a winner
        elif db.query.get_count(Horse, query_data):
            raise ModelStateError(
                "Unable to set winner. Race already has a registered winner.",
                context=context)

        Horse.update_one(winner_data, horse_id)

        return {'message': 'Winner set.'}

    @staticmethod
    def set_scratched(horse_id: dict) -> dict:
        if Horse.is_scratched(horse_id):
            raise ModelStateError(
                'Horse has already been scratched.',
                context=ModelStateError.get_error_context(horse_id=horse_id))

        if Horse.is_winner(horse_id):
            raise ModelStateError(
                'This horse is marked as a winner, cannot scratch the race winner.',
                context=ModelStateError.get_error_context(horse_id=horse_id))

        scratched_data = {
            Horse.Status.LABEL.value: Horse.Status.SCRATCHED.value
        }

        Horse.update_one(scratched_data, horse_id)

        return {'message': 'Horse scratched.'}

    @staticmethod
    def is_winner(horse_id: dict) -> bool:

        horse_data = Horse.get_data(horse_id, 'winner')

        return horse_data['winner'] == Horse.WINNER

    @staticmethod
    def is_scratched(horse_id: dict) -> bool:

        horse_data = Horse.get_data(horse_id, 'scratched')
        return horse_data['scratched'] == Horse.Status.SCRATCHED.value
