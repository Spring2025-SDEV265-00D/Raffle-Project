from flask import Blueprint, jsonify
from flask_cors import cross_origin

from models import Ticket
from utils import validate_payload_structure  #, restrict_by_role

cashier_bp = Blueprint("cashier", __name__, url_prefix="/redeem")
# cashier_bp.before_request(restrict_by_role("Cashier"))


@cashier_bp.route("/ticket", methods=["POST"])
@validate_payload_structure(expected_fields=['ticket_id', 'request'])
@cross_origin()
def ticket_update(validated_payload):
    return jsonify(Ticket.update_standing(validated_payload)), 200
