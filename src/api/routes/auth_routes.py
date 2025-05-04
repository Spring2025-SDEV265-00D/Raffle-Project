from flask import Blueprint, request, jsonify, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from datetime import timedelta
from werkzeug.security import generate_password_hash

from models import User, Role
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


@auth_bp.route("/register", methods=["POST"])
@login_required
def register_user():
    try:
        # Check if current user is admin
        if current_user.get_role()['role'] != 'Admin':
            return jsonify({
                "status": "error",
                "message": "Only administrators can register new users."
            }), 403

        # Get form data
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')

        # Validate required fields
        if not all([username, password, role]):
            return jsonify({
                "status": "error",
                "message": "All fields are required."
            }), 400

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Get role ID based on role name
        role_id = None
        for role_enum in Role.Tier:
            if role_enum.label == role:
                role_id = role_enum.value
                break

        if not role_id:
            return jsonify({
                "status": "error",
                "message": "Invalid role specified."
            }), 400

        # Create user data
        user_data = {
            'username': username,
            'password': hashed_password,
            'role_id': role_id,
            'last_login_dttm': None  # Add this field
        }

        try:
            # Add user to database
            new_user = User.add(user_data)
            return jsonify({
                "status": "success",
                "message": "User registered successfully",
                "user": {
                    "username": new_user['username'],
                    "role": Role.Tier(new_user['role_id']).label
                }
            }), 201
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Error creating user: {str(e)}"
            }), 500

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
