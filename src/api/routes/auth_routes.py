from flask import Blueprint, request, jsonify, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from datetime import timedelta

from models import User
from utils import validate_payload_structure
# set blueprint
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")






@auth_bp.route("/login", methods=["POST"])
def login():

    username = request.form.get('username')
    password = request.form.get('password')

    user = User.login({'username': username, 'password': password})
    login_user(user)

    return jsonify({
        "status": "success",
        "message": f"Login successful! Hello {user.username}",
        "role": user.get_role(),
        "username": user.username
    }), 200



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
            "role": current_user.get_role(),
            "username": current_user.username
        }), 200
    except Exception as e:

        return jsonify({
            "status": "error",
            "message": "Error retrieving user role."
        }), 500
