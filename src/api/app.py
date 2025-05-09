import os
import secrets

from datetime import timedelta
from flask import Flask, jsonify
from flask_cors import CORS
from flask_login import LoginManager
from dotenv import load_dotenv

from models import User
from routes import blueprints
from utils import AppError

from utils.db_instance import initialize_db

load_dotenv()

app = Flask(__name__)

for each in blueprints:
    app.register_blueprint(each)

# CORS(app)
origins = os.getenv("FRONT_END_ORIGINS")
if origins:
    origins = [o.strip() for o in origins.split(",")]
else:
    origins = "*"

CORS(app, origins=origins)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

# Generate a secure secret key. We do not need to set this manually.
app.secret_key = secrets.token_hex(32)


@app.after_request
def apply_cors_headers(response):
    response.headers.setdefault("Access-Control-Allow-Credentials", "true")
    return response


with app.app_context():
    initialize_db()

# set up login manager
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.unauthorized_handler
def unauthorized():
    return jsonify({"error": "Authentication required"}), 401


# load user for flask-login
@login_manager.user_loader
def load_user(user_id):
    return User.load(user_id)


@app.teardown_appcontext
def close_db(e=None):
    from utils import db
    db.close_conn(e)


# *====================GLOBAL CONTEXT ERROR HANDLER====================*


@app.errorhandler(AppError)
def handle_app_error(error):
    response, status = error.format(error)
    return {"error": response['error']}, status


if __name__ == "__main__":
    app.run(debug=True, port=5000)
