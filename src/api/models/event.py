from .base_model import BaseModel


class Event(BaseModel):

    @staticmethod
    def get_races(data: dict, filter="all"):
        from .race import Race
        if Event.id_exists_in_db(data):
            return Race.get_races_for_event(data, filter)
