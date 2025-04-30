import os
import secrets

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

CORS(app, origins=[os.getenv("FRONT_END_ORIGIN")])

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
    # response.headers["Access-Control-Allow-Credentials"] = "true"
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
def handle_app_error(e):
    from utils.util import Util

    response, status = AppError.format(e)

    Util.pretty_print(response)
    return jsonify(response['error']), status
    """ #!let it crash for now so we can see whats going on
# for unexpected errors?
@app.errorhandler(Exception)
def handle_unexpected_error(e):
    return jsonify({"error": "Something UNEXPECTED went wrong"}), 500
 """


if __name__ == "__main__":
    app.run(debug=True, port=5000)
