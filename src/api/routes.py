from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from dotenv import load_dotenv
import os

from models import Event
from models import Race
from models import Horse
from models import Ticket
from models import User

from utils import Util
from utils import AppError
from utils import validate_payload_structure
from utils.db_instance import initialize_db


#############################################

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes - remove if not needed
load_dotenv()
app.secret_key = os.getenv("SECRET_KEY")


with app.app_context():
    initialize_db()


# set up login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# load user for flask-login
@login_manager.user_loader
def load_user(user_id):
    return User.load(user_id)


@app.route("/login", methods=["POST", "GET"])
# @validate_payload_structure(expected_fields=['username', 'password'])
def login():  # validated_payload):

    validated_payload = {'username': 'admin', 'password': 'admin123'}
    user = User.login(validated_payload)
    login_user(user)

    return jsonify({"message": "Login successful"})


""" 
@app.route("/huhu")
@login_required
def test():
    Util.p("in test routes", current_user=repr(current_user))

    return current_user """

# *====================ADMIN====================*


@app.route("/admin/events/create", methods=["POST"])
@validate_payload_structure(expected_fields=['event_name',
                                             'location',
                                             'start_date',
                                             'end_date'])
def create_event(validated_payload):

    return jsonify(Event.create(validated_payload)), 200

    # ?---------------------------------------------------------------------------------------


@app.route("/admin/races/close", methods=["PATCH"])
@validate_payload_structure(expected_fields='race_id')
@cross_origin()
def close_race(validated_payload):

    # Util.p("in close raace route api", validated_payload=validated_payload)

    return jsonify(Race.close(validated_payload)), 200

    # ?---------------------------------------------------------------------------------------

    # *====================SELLERS====================*


@app.route("/ticket/purchase", methods=["POST"])
@validate_payload_structure(expected_headers='order', expected_nested=['race_id', 'qtty'])
@cross_origin()
# arg passed by validation decorator
def ticket_purchase(validated_payload):

    response = {'order': Ticket.batching(validated_payload['order'])}

    # for ticket_unit in response["order"]:
    # Util.p("response api->web ", ticket_printable_data=ticket_unit)  # debug

    return jsonify(response), 201  #

    # ?---------------------------------------------------------------------------------------


@app.route("/ticket/update", methods=["POST"])
@validate_payload_structure(expected_fields=['ticket_id', 'request'])
@cross_origin()
def ticket_update(validated_payload):

    # Util.p("api route tik update", validated_payload=validated_payload)

    # ticket_data = {'ticket_id': 22, 'request': "refund"}

    # return jsonify(Ticket.update_standing(ticket_data)), 200
    return jsonify(Ticket.update_standing(validated_payload)), 200

    # ?---------------------------------------------------------------------------------------

    # *====================FETCHERS====================*


@app.route("/ticket/info", methods=["GET"])
@validate_payload_structure(expected_fields='ticket_id')
@cross_origin()
def fetch_ticket(validated_payload):

    filter = None

    return jsonify(Ticket.get_data(validated_payload))

    # ?---------------------------------------------------------------------------------------

    # todo: merge events/info and events? need update


@app.route("/event/info", methods=["GET"])
@validate_payload_structure(expected_fields='event_id')
@cross_origin()
def fetch_event(validated_payload):

    filter = None
    return jsonify(Event.get_data(validated_payload, filter))

    # ?---------------------------------------------------------------------------------------


@app.route("/events", methods=["GET"])
@validate_payload_structure(expecting_payload=False)
@cross_origin()
def fetch_all_events(validated_payload=None):
    """Fetches all available event data.

Args:
    None.

Returns:
    Response: JSON array of event objects

    Example:
        [
            {
                "id": 1,
                "event_name": "St Patrick Fair 2022",
                "location": "Lafayette",
                "start_date": "2022-01-01",
                "end_date": "2022-01-03"
            },
            {
                "id": 2,
                "event_name": "Lilly Fair 2022",
                "location": "Lafayette",
                "start_date": "2022-01-05",
                "end_date": "2022-01-08"
            }
        ]
    """

    Util.p("in routes", validated_payload=validated_payload)  # debug

    filter = None  # set filter with expected attributes
    return jsonify(Event.get_all(filter))

    # ?---------------------------------------------------------------------------------------


@app.route("/events/races", methods=["GET"])
@validate_payload_structure(expected_fields='event_id')
@cross_origin()
def fetch_races_for_event(validated_payload):

    # todo: implement filter if case needed
    # todo: (expect 'status' for "all" or "open" to fetch all or open only races)
    # todo: ensures staff can only sell tickets for open race.
    # todo: If front is adjusted to display which races are closed this is not needed

    # if status is None:
    #   status = "all"

    # Util.p("fetch races route", incoming=request.args.to_dict())
    # Util.p("fetch races route", validated_payload=validated_payload)

    # (validated_payload))
    return jsonify(Event.get_races(validated_payload))
    # ?---------------------------------------------------------------------------------------


@app.route("/events/races/horses", methods=["GET"])
@validate_payload_structure(expected_fields='race_id')
def fetch_horses_for_race(validated_payload):

    # can take a filter to fetch only specific data
    filter = None

    return jsonify(Race.get_horses(validated_payload, filter))
    #!# *====================DEBUGGIN====================*


@app.route("/", methods=["GET"])
def testing():

    # data = {"order": [{"race_id": 1, "qtty": 3}, {"race_id": 2, "qtty": 2}],
    #       "status": [{'s1': "S1", 's2': "S2"}, {'s1': "S3", 's2': "S4"}]}

    data = Race.get_horses({'race_id': 1})
    return jsonify(data)
    #!# *====================DEBUGGIN====================*

    #!deprecated below this point, here just for reference################################################!!!!

#########


@app.route("/ticket/status", methods=["GET"])
@cross_origin()
def ticket_status():

    # get data from url parameter
    reference_number = request.args.get("reference_number")

    if not reference_number:
        return jsonify({"error": "Reference number is required."}), 400

    ticket_data = Ticket.get_data(reference_number)

    # extracts value and updates it to a printable str for front end
    status_value = ticket_data.get("status_code")
    ticket_data["status_code"] = Ticket.Status(status_value).label

    # sending all ticket data, send only what is needed?
    return jsonify(ticket_data)

    # *====================DATABASE====================*


@app.teardown_appcontext
def close_db(e=None):
    from utils import db

    db.close_conn(e)

    # *====================GLOBAL CONTEXT ERROR HANDLER====================*


@app.errorhandler(AppError)
def handle_app_error(e):
    from utils.util import Util

    response, status = AppError.format(e)

    Util.pretty_print(response)
    return jsonify(response['error']), status

    """ #!let it crash for now so we can see whats going on
# for unexpected errors?
@app.errorhandler(Exception)
def handle_unexpected_error(e):
    return jsonify({"error": "Something UNEXPECTED went wrong"}), 500
 """


if __name__ == "__main__":
    app.run(debug=True, port=5000)
