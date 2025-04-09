from flask import Flask, request, jsonify
from flask_cors import CORS  # Import this if you need to handle CORS
from flask_cors import cross_origin


import sqlite3
from models.ticket import Ticket  # Updated import statement
from models.event import Event
from models.race import Race
from models.horse import Horse
from utils.util import Util
from utils.app_error import AppError
from utils.decorator import *

from utils.db_instance import db

#############################################

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes - remove if not needed


"""
todo set routes.py for new functionality   
todo add admin functionality

todo: implement debugger decorator

batchin:
    backend batching ok, need front end
    -added check for closed races in batching


    next:
    -Operations Manager:
***need to commit for db inserts

    //    -Add event - ok 
        edit event 
        
        
      **expects frontend data such as {event_id : N, qtty: n} where n, is the # of horses to add in that race
        
        -delete/edit races
            -Cascade on delete? ->will produce several race and horse _id gaps over time (matters?)
            -for editing we can add n horses or pop the n last ones (or wipe the race and build new)
        
    //    -Stop betting (close_race)-- ok -> 
        -Scratch horse by (horse_num? the last inserted horse? does it matter?)

"""


# *====================ADMIN====================*


@app.route("/admin/events/create", methods=["POST"])
@validate_payload_structure(expected_fields=['event_name',
                                             'location',
                                             'start_date',
                                             'end_date'])
def create_event(validated_payload):
    """Creates a new event using the provided event data.


Args:
    JSON:
        -payload with the following required keys:
        - event_name (str): Name of the event.
        - location (str): Location where the event takes place.
        - start_date (str): Event start date in 'YYYY-MM-DD' format.
        - end_date (str): Event end date in 'YYYY-MM-DD' format.

    Example:
        {
            "event_name": "Test Fair 2025",
            "location": "Some Place",
            "start_date": "2025-09-01",
            "end_date": "2025-09-04"
        }

Raises:
    PayloadError: If the payload is missing any required keys. Raised by Util.check_payload().


Returns:
    Response: JSON with successfuly created event or error message

    Success Response (HTTP 200):
    {
    "end_date": "2025-09-04",
    "event_name": "Test Fair 2025",
    "id": 7,
    "location": "Some Place",
    "start_date": "2025-09-01"
    }

    Error Response (HTTP 400):
        {
        "error": "Payload Error: Missing or mismatching keys.['missing_keys']"
        }

    """

    return jsonify(Event.create(validated_payload)), 200

# ?---------------------------------------------------------------------------------------


""" @app.route("/admin/events/race/create", methods=["POST"])
@validate_payload_structure(expected_fields=
def create_race(validated_payload) """
# todo current 'add_race()' functionality takes a race_id and qtty of horses to add
# todo need adjustment
# ?---------------------------------------------------------------------------------------


@app.route("/admin/races/close", methods=["PATCH"])
@validate_payload_structure(expected_fields='race_id')
@cross_origin()
def close_race(validated_payload):
    """Closes betting for a specific race.

Args:
    JSON payload with a required 'race_id' key.

    Example:
        {
            "race_id": 1
        }


Raises:
    PayloadError: If the payload is missing any required keys. Raised by Util.check_payload().


Returns:
    Response: JSON object indicating the result of the close operation.

    Success Response (HTTP 200):
        {
            "message": "Race -> {'race_id': 1} has been closed. It is no longer available for participation."
        }

    Error Response (HTTP 400):
        {
        "error": "Payload Error: Missing or mismatching keys.['missing_keys']"
        }

        Model State Error (HTTP 400 or 409):
            {
                "error": "Model State Error: Race -> {'race_id': 1} has already been closed."
            }
    """

    Util.p("in close raace route api", validated_payload=validated_payload)

    return jsonify(Race.close(validated_payload)), 200


# ?---------------------------------------------------------------------------------------


# *====================SELLERS====================*


@app.route("/ticket/purchase", methods=["POST"])
@validate_payload_structure(expected_headers='order', expected_nested=['race_id', 'qtty'])
@cross_origin()
def ticket_purchase(validated_payload):  # arg passed by validation decorator
    """Processes ticket purchase request for multiple races.

Args:
    JSON payload with an 'order' key containing batch data.

    Batch Data:
        {
            "order": [
                {"race_id": 1, "qtty": 3},
                {"race_id": 2, "qtty": 2},
                ...
            ]
        }

Returns:
    JSON response with generated ticket data for each requested ticket.

    Ticket Data:
        {
            "order": [
                {
                    "created_dttm": "2025-04-04 17:40:43",
                    "event_name": "St Patrick Fair 2022",
                    "horse_number": 6,
                    "id": 255,
                    "race_number": 1
                },
                {
                    "created_dttm": "2025-04-04 17:40:43",
                    "event_name": "St Patrick Fair 2022",
                    "horse_number": 2,
                    "id": 256,
                    "race_number": 1
                },
                ...
            ]
        }
"""

    response = {'order': Ticket.batching(validated_payload['order'])}

    # for ticket_unit in response["order"]:
    # Util.p("response api->web ", ticket_printable_data=ticket_unit)  # debug

    return jsonify(response), 201  #

# ?---------------------------------------------------------------------------------------

# *====================FETCHERS====================*


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
    """Fetches all races associated with a given event.

Args:
    event_id (int or str): Required. Provided as a URL query parameter.
    status (str, optional): Optional query parameter to filter races.
        - "open": Return only races that are still open.
        - "all": Return all races (default).

    Example Request:
        /events/races?event_id=1&status=open

Returns:
    Response: JSON array of race objects for the given event.

    Example:
        [
            {
                "id": 1,
                "event_id": 1,
                "race_number": 1,
                "closed": 0
            },
            {
                "id": 2,
                "event_id": 1,
                "race_number": 2,
                "closed": 0
            }
        ]
    """

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


@app.route("/ticket/cancel", methods=["POST"])  # ! not sure if this is needed
def ticket_refund():

    data = request.get_json()

    return jsonify(Ticket.cancel(data)), 200

    ############################# Tried and Tested #############################

#


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
