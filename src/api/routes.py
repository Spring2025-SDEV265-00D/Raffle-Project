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
add error handling
add admin functionality

backend batching ok, need front end

    next:
    -Operations Manager:
        -Add event - ok 
        -delete/edit event ?
            -IF delete, prob need cascade delete (db schema update)
        
        -Add race with horses to event
        -delete/edit races
            -Cascade on delete? ->will produce several race and horse _id gaps over time (matters?)
            -for editing we can add n horses or pop the n last ones (or wipe the race and build new)
        
        -Stop betting (close_race)
        -Scratch horse by (horse_num? the last inserted horse? does it matter?)

"""


@app.route("/test", methods=["GET"])
def testing():

    data = {"ticket_id": 13}
    # Event.get_races(data)  # Event.get_races(data)
    data = Event.build_event(data)

    return jsonify(data)

    ############################# Tried and Tested #############################


@app.route("/events/races", methods=["GET"])  # ok
def fetch_all_event_races():

    # data = {'event_id' : someINTorSTR}

    label = Event.Fields.ID.label
    event_id = request.args.get(label)
    data = {label: event_id}

    status = request.args.get("status")

    data = {label: 4}  # debug

    # status dictates whether we return all or only active races. "open" = only open races, "all" = all races
    # default is all
    if status is None:
        status = "all"

    return jsonify(Event.get_races(data, status))


@app.route("/events", methods=["GET"])
def fetch_all_events():
    """ Fetches all row data for all events in db
        Takes no data

    Returns:
        _type_: list[dict] | dict
    """
    # no incoming data

    filter = None  # set filter with expected attributes
    return jsonify(Event.get_all(filter))


@app.route("/ticket/purchase", methods=["POST"])
@cross_origin()
def ticket_purchase():

    data = request.get_json()
    # data = {"order": [{"race_id": 1, "qtty": 3}, {"race_id": 2, "qtty": 2}]}

    Util.p("data incoming web->api", data=data)

    if not data or "order" not in data:
        return jsonify({"error": "Error in payload."}), 400

    data["order"] = Ticket.batching(data["order"])

    for ticket_unit in data["order"]:
        Util.p("response api->web ", ticket_printable_data=ticket_unit)  # debug
    return jsonify(data), 201  # {"error": "TEEEST."}


@app.route("/ticket/cancel", methods=["POST"])
def ticket_cancelation():

    data = request.get_json()

    return jsonify(Ticket.cancel(data)), 200

    ############################# Tried and Tested #############################


@app.route("/admin/stop-betting", methods=["POST"])
@cross_origin()
def stop_betting():

    data = request.get_json()
    race_id = data.get("race_id")

    if not race_id:
        return jsonify({"error": "Race not found"})  # needs upd

    return jsonify(Race.stop_betting(race_id))


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


@app.teardown_appcontext
def close_db(e=None):
    db.close_conn(e)


@app.errorhandler(AppError)
def handle_app_error(e):
    from utils.util import Util

    response, status = e.format()

    Util.pretty_print(response)
    return jsonify(response), status


""" 
# for unexpected errors?
@app.errorhandler(Exception)
def handle_unexpected_error(e):
    return jsonify({"error": "Something UNEXPECTED went wrong"}), 500
 """

if __name__ == "__main__":
    app.run(debug=True, port=5000)
