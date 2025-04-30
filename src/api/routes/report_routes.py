from flask import Blueprint, request, jsonify
from flask_login import login_required
from flask_cors import CORS, cross_origin

from models import Race
from utils import Report
from utils import validate_payload_structure, restrict_by_role

# set blueprint
report_bp = Blueprint("report", __name__, url_prefix="/report")
report_bp.before_request(restrict_by_role("Admin"))


# ? by Race
@report_bp.route("/race", methods=["GET", "POST"])
@validate_payload_structure(expected_fields='race_id')
def race_report(validated_payload):

    # validated_payload = {'race_id': 1}

    return jsonify(Report.by_race(validated_payload)), 200
