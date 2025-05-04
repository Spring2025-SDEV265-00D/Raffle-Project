from flask import Blueprint, jsonify
from flask_cors import cross_origin

from utils import validate_payload_structure  #, require_role, restrict_by_role
from models import Event
from models import Race
from models import Horse
from utils import db

# set blueprint
admin_bp = Blueprint("admin", __name__, url_prefix="/admin")
# admin_bp.before_request(restrict_by_role("Admin"))


@admin_bp.route("/events/create", methods=["POST"])
@cross_origin()
@validate_payload_structure(
    expected_fields=['event_name', 'location', 'start_date', 'end_date'])
def create_event(validated_payload):

    return jsonify(Event.add(validated_payload)), 200


@admin_bp.route("/races/create", methods=["POST"])
@cross_origin()
@validate_payload_structure(expected_fields=['event_id', 'race_number'])
def create_race(validated_payload):
    return jsonify(Race.add(validated_payload)), 200


@admin_bp.route("/races/close", methods=["PATCH"])
@validate_payload_structure(expected_fields='race_id')
@cross_origin()
def close_race(validated_payload):
    return jsonify(Race.close(validated_payload)), 200


@admin_bp.route("/races/delete", methods=["DELETE"])
@validate_payload_structure(expected_fields='race_id')
@cross_origin()
def delete_race(validated_payload):
    try:
        Race.delete_by_id(validated_payload)
        return jsonify({
            "status": "success",
            "message": f"Race {validated_payload['race_id']} has been deleted successfully"
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Failed to delete race: {str(e)}"
        }), 500


@admin_bp.route("/race/update", methods=["POST", "GET"])
@cross_origin()
@validate_payload_structure(expected_fields=['horse_id', 'request'])
def update_race(validated_payload):
    return jsonify(Race.update(validated_payload)), 200


#!this route might need front end to check for horse_num duplicates (for races too)
@admin_bp.route("/horses/create", methods=["POST", "GET"])
@cross_origin()
@validate_payload_structure(expected_fields=['race_id', 'horse_number'])
def create_horse(validated_payload):
    return jsonify(Horse.add(validated_payload)), 200
