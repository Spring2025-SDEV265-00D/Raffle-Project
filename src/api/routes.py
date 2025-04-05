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

from utils.db_instance import db

#############################################

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes - remove if not needed


"""
todo
    set routes.py for new functionality




add admin functionality

batchin:
    backend batching ok, need front end
    -added check for closed races in batching


    next:
    -Operations Manager:
***need to commit for db inserts
todo:

    //    -Add event - ok 
        edit event 
        
    //   -Add race with horses to event - ok, done in transaction Event.add_races
      *          **currently handles only a single race -> need update to handle multiple races if case valid
       *         **expects frontend data such as {event_id : N, qtty: n} where n, is the # of horses to add in that race
        
        -delete/edit races
            -Cascade on delete? ->will produce several race and horse _id gaps over time (matters?)
            -for editing we can add n horses or pop the n last ones (or wipe the race and build new)
        
    //    -Stop betting (close_race)-- ok -> 
        -Scratch horse by (horse_num? the last inserted horse? does it matter?)

"""
# todo : add check payload to routes

# *====================ADMIN====================*


@app.route("/admin/events/create", methods=["POST"])  # !is post
def create_event():
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

    data = Util.valid_payload(request.get_json(), expected=[
        'event_name', 'location', 'start_date', 'end_date'])

    return jsonify(Event.create(data)), 200


# ?---------------------------------------------------------------------------------------


@app.route("/admin/races/close", methods=["POST"])
@cross_origin()
def close_race():
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

    data = Util.valid_payload(request.get_json(), expected=['race_id'])

    return jsonify(Race.close(data)), 200


# ?---------------------------------------------------------------------------------------


# *====================SELLERS====================*


@app.route("/ticket/purchase", methods=["POST"])
@cross_origin()
def ticket_purchase():
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

    data = request.get_json()
    # data = {"order": [{"race_id": 1, "qtty": 3}, {"race_id": 2, "qtty": 2}],
    #       "status": [{'s1': "S1", 's2': "S2"}, {'s1': "S3", 's2': "S4"}]}

#    data = Util.valid_nested_payload(
 #       data,
  #      ['order', 'status'],
   #     [['race_id', 'qtty'], ['s1', 's2']])

    # Util.p("data incoming web->api", data=data)

    data["order"] = Ticket.batching(data["order"])

   # for ticket_unit in data["order"]:
    #   Util.p("response api->web ", ticket_printable_data=ticket_unit)  # debug
    return jsonify(data), 201  # {"error": "TEEEST."}

# *====================FETCHERS====================*


@app.route("/events", methods=["GET"])
def fetch_all_events():
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

    filter = None  # set filter with expected attributes
    return jsonify(Event.get_all(filter))


# ?---------------------------------------------------------------------------------------


@app.route("/events/races", methods=["GET"])  # ok
def fetch_all_event_races():
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

    data = {'event_id': request.args.get('event_id')}
    #!data = {'event_id': 1}
    status = request.args.get("status")

    if status is None:
        status = "all"

    return jsonify(Event.get_races(data, status))
# ?---------------------------------------------------------------------------------------

#!# *====================DEBUGGIN====================*


@app.route("/", methods=["GET"])
def testing():

    data = {"order": [{"race_id": 1, "qtty": 3}, {"race_id": 2, "qtty": 2}],
            "status": [{'s1': "S1", 's2': "S2"}, {'s1': "S3", 's2': "S4"}]}

    data = Util.valid_nested_payload(data,
                                     expected_headers=['order', 'status'],
                                     expected_nested=[['race_id', 'qtty'], ['s1', 's2']])
    return jsonify(data)
#!# *====================DEBUGGIN====================*


@app.route("/ticket/cancel", methods=["POST"])  # ! not sure if this is needed
def ticket_cancelation():

    data = request.get_json()

    return jsonify(Ticket.cancel(data)), 200

    ############################# Tried and Tested #############################

#


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


""" 
# for unexpected errors?
@app.errorhandler(Exception)
def handle_unexpected_error(e):
    return jsonify({"error": "Something UNEXPECTED went wrong"}), 500
 """

if __name__ == "__main__":
    app.run(debug=True, port=5000)
