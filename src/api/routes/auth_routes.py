from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user


from models import User
from utils import validate_payload_structure
# set blueprint
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=["POST", "GET"])
@validate_payload_structure(expected_fields=['username', 'password'])
def login(validated_payload):

    # validated_payload = {'username': 'admin', 'password': 'admin123'}
    user = User.login(validated_payload)
    login_user(user)

    return jsonify({"message": f"Login successful! Hello {user.username}"}), 200


@auth_bp.route("/logout", methods=["POST", "GET"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout successful!"}), 200


@auth_bp.route("/me", methods=["GET"])
@login_required
def get_user_role():

    return current_user.get_role_str(), 200
