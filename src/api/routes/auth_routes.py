from flask import Blueprint, request, jsonify, current_app
from flask_login import login_user, logout_user, login_required, current_user
from datetime import timedelta

from models import User
from utils import validate_payload_structure
# set blueprint
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=["POST"])
@validate_payload_structure(expected_fields=['username', 'password'])
def login(validated_payload):
    try:
        # Get credentials from form data
        username = request.form.get('username')
        password = request.form.get('password')

        # Attempt to authenticate the user
        user = User.login({'username': username, 'password': password})
        if not user:
            return jsonify({
                "status": "error",
                "message": "Invalid credentials. Please try again."
            }), 401

        # Set session timeout to 30 minutes
        login_user(user, duration=timedelta(minutes=30))

        return jsonify({
            "status": "success",
            "message": f"Login successful! Hello {user.username}"
        }), 200

    except Exception as e:
        # Log the error here if you have logging set up
        return jsonify({
            "status":
            "error",
            "message":
            "An error occurred during login. Please try again."
        }), 500


@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    try:
        logout_user()
        return jsonify({
            "status": "success",
            "message": "Logout successful!"
        }), 200
    except Exception as e:
        # Log the error here if you have logging set up
        return jsonify({
            "status": "error",
            "message": "An error occurred during logout."
        }), 500


@auth_bp.route("/me", methods=["GET"])
@login_required
def get_user_role():
    try:
        return jsonify({
            "status": "success",
            "role": current_user.get_role()
        }), 200
    except Exception as e:
        # Log the error here if you have logging set up
        return jsonify({
            "status": "error",
            "message": "Error retrieving user role."
        }), 500
