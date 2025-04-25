from flask import Blueprint, request, jsonify
from flask_login import login_required
from flask_cors import CORS, cross_origin

from utils import validate_payload_structure
from models import Event
from models import Race
from models import Horse


# set blueprint
admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


# ? events


@admin_bp.route("/events/create", methods=["POST"])
@login_required
@cross_origin()
@validate_payload_structure(expected_fields=['event_name', 'location', 'start_date', 'end_date'])
def create_event(validated_payload):

    return jsonify(Event.add(validated_payload)), 200


# ? RACES

@admin_bp.route("/races/create", methods=["POST"])
@cross_origin()
@validate_payload_structure(expected_fields=['event_id', 'race_number'])
def create_race(validated_payload):
    # def add_race():
    # validated_payload = {'event_id': 1, 'race_number': 999}
    return jsonify(Race.add(validated_payload)), 200


@admin_bp.route("/races/close", methods=["PATCH"])
@validate_payload_structure(expected_fields='race_id')
@login_required
@cross_origin()
def close_race(validated_payload):

    # Util.p("in close raace route api", validated_payload=validated_payload)

    return jsonify(Race.close(validated_payload)), 200


@admin_bp.route("/race/update", methods=["POST", "GET"])
@login_required
@cross_origin()
@validate_payload_structure(expected_fields='horse_id')
def set_race_winner(validated_payload):

    # validated_payload = {'horse_id': '1'}

    return jsonify(Horse.set_winner(validated_payload)), 200


# ? horses


#!this route might need front end to check for horse_num duplicates (for races too)
@admin_bp.route("/horses/create", methods=["POST", "GET"])
@cross_origin()
@validate_payload_structure(expected_fields=['race_id', 'horse_number'])
def create_horse(validated_payload):

    # validated_payload = {'race_id': 1, 'horse_number': 999}
    return jsonify(Horse.add(validated_payload)), 200
