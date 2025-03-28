from flask import Flask, request, jsonify
from flask_cors import CORS  # Import this if you need to handle CORS
from flask_cors import cross_origin


import sqlite3
from models.ticket import Ticket  # Updated import statement
from models.event import Event
from models.race import Race
from models.horse import Horse
from utils.util import Util
from utils.error import Error

from utils.db_instance import db

#############################################

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes - remove if not needed


# receives race_id from front end
# functional batching route, needs front end
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
        Util.p("response api->web ", ticket_printable_data=ticket_unit)

    return jsonify(data), 201  # {"error": "TEEEST."}


# routes are broken below this point
#


@app.route("/events", methods=["GET"])
def fetch_all_events():
    return jsonify(Event.get_all())


@app.route("/events/races", methods=["GET"])
def fetch_all_event_races():

    event_id = request.args.get("event_id")
    status = request.args.get("status")

    # status dictates whether we return all or only active races. "open" = only open races, "all" = all races
    # default is all
    if status is None:
        status = "all"

    return jsonify(Event.get_races(event_id, status))


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


@app.route("/ticket/cancel", methods=["POST"])
def ticket_cancelation():

    data = request.get_json()
    reference_number = data.get("reference_number")

    return jsonify(Ticket.cancel(reference_number))


@app.teardown_appcontext
def close_db(e=None):
    db.close_conn(e)


@app.errorhandler(Error)
def handle_app_error(e):
    response, status = e.format()
    return jsonify(response), status


if __name__ == "__main__":
    app.run(debug=True, port=5000)
