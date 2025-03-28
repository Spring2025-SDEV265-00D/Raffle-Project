from utils.base_model import BaseModel


class Event(BaseModel):

    @staticmethod
    def get_races(event_id, filter="all"):
        from models.race import Race

        return Race.get_races_for_event(event_id, filter)
