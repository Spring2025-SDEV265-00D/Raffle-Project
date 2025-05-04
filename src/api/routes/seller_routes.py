from flask import Blueprint, jsonify
from flask_cors import cross_origin

from models import Ticket
from utils import validate_payload_structure  #, restrict_by_role

seller_bp = Blueprint("seller", __name__, url_prefix="/pos")
# seller_bp.before_request(restrict_by_role("Seller"))


@seller_bp.route("/ticket/purchase", methods=["POST"])
@validate_payload_structure(expected_headers='order',
                            expected_nested=['race_id', 'qtty'])
@cross_origin()
def ticket_purchase(validated_payload):

    response = {'order': Ticket.batching(validated_payload['order'])}

    # for ticket_unit in response["order"]:
    # Util.p("response api->web ", ticket_printable_data=ticket_unit)  # debug

    return jsonify(response), 201
