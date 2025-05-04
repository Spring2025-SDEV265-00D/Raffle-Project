from .base_meta import BaseMeta
from .base_model import BaseModel
from .event import Event
from .horse import Horse
from .race import Race
from .ticket import Ticket
from .user import User

# used to check if a parent exists before adding a child (ensuring you can't add a race to an invalid event_id)
MODEL_REGISTRY = {
    'event_id': Event,
    'race_id': Race,
    'horse_id': Horse,
    'ticket_id': Ticket
}
