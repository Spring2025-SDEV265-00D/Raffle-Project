from models import Ticket
from flask import Blueprint, request, jsonify
from flask_cors import CORS, cross_origin
from flask_login import login_required

from models import Event
from models import Race
from utils import validate_payload_structure, require_role

fetcher_bp = Blueprint("fetcher", __name__, url_prefix="/fetch")

# need to replace @login_required with @require_role decorator where needed
# *EVENTS


@fetcher_bp.route("/event/info", methods=["GET"])
@validate_payload_structure(expected_fields='event_id')
@login_required
@cross_origin()
def fetch_event(validated_payload):

    filter = None
    return jsonify(Event.get_data(validated_payload, filter))


@fetcher_bp.route("/events", methods=["GET"])
@validate_payload_structure(expecting_payload=False)
@login_required
@cross_origin()
def fetch_all_events(validated_payload=None):

    # Util.p("in routes", validated_payload=validated_payload)  # debug

    filter = None  # set filter with expected attributes
    return jsonify(Event.get_all(filter))


# *RACES


@fetcher_bp.route("/events/races", methods=["GET"])
@validate_payload_structure(expected_fields='event_id')
@login_required
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


# *HORSES


# !this is admin functionality
@fetcher_bp.route("/events/races/horses", methods=["GET"])
@validate_payload_structure(expected_fields='race_id')
@require_role('Admin')
def fetch_horses_for_race(validated_payload):

    # validated_payload = {'race_id': 1}
    # can take a filter to fetch only specific data
    filter = None
    return jsonify(Race.get_horses(validated_payload, filter))


# *TICKETS


@fetcher_bp.route("/ticket/info", methods=["GET"])
@validate_payload_structure(expected_fields='ticket_id')
@login_required
@cross_origin()
def fetch_ticket(validated_payload):

    filter = None
    return jsonify(Ticket.get_data(validated_payload, filter)), 200
