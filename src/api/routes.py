from flask import Flask, request, jsonify
from flask_cors import CORS  # Import this if you need to handle CORS
from flask_cors import cross_origin


import sqlite3
from models.ticket import Ticket  # Updated import statement
from models.event import Event
from models.race import Race

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes - remove if not needed


# to do
# reprint ticket


@app.route("/test", methods=["GET"])
def get_data():

    return jsonify({"data": "Hello, World!"})


@app.route("/events", methods=["GET"])
def fetch_all_events():
    return jsonify(Event.get_all_events())


@app.route("/events/races", methods=["GET"])
def fetch_all_event_races():

    event_id = request.args.get("event_id")

    return jsonify(Event.get_races(event_id))


@app.route("/ticket/status", methods=["GET"])
@cross_origin()
def ticket_status():

    # get data from url parameter
    reference_number = request.args.get("reference_number")
    # validate
    if not reference_number:
        return jsonify({"error": "Reference number is required."}), 400

    #
    status_data = Ticket.get_status(reference_number)
    # print(status_data)

    return jsonify(status_data)


# receives race_id from front end
@app.route("/ticket/purchase", methods=["POST"])
def ticket_purchase():

    data = request.get_json()
    race_id = data.get("race_id")

    if not race_id:
        return jsonify({"error": "Reference number is required."}), 400

    return jsonify(Ticket.create_ticket(race_id)), 201


@app.route("/ticket/cancel", methods=["POST"])
def ticket_cancelation():

    data = request.get_json()
    reference_number = data.get("reference_number")

    return jsonify(Ticket.cancel_ticket(reference_number))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
