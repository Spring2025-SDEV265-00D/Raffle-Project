from flask import Blueprint, jsonify
from reports import Report
from utils import validate_payload_structure  #, restrict_by_role

# set blueprint
report_bp = Blueprint("report", __name__, url_prefix="/report")
# report_bp.before_request(restrict_by_role("Admin"))


@report_bp.route("/race", methods=["GET", "POST"])
@validate_payload_structure(expected_fields='race_id')
def race_report(validated_payload):
    return jsonify(Report.by_race(validated_payload)), 200
