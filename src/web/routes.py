from flask import Flask, render_template
from dotenv import load_dotenv
import os
from auth import check_auth

load_dotenv()
API_BASE_URL = os.getenv("API_BASE_URL")

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")  # needed for sessions


# This will add the API_BASE_URL to the context of the app,
# so that all of the templates can access it.
@app.context_processor
def inject_globals():
    return dict(api_base_url=API_BASE_URL)


# *-----------------LOGIN-----------------*
@app.route("/login")
def login():
    return "Login page not implemented yet. Should POST username/password to API_BASE_URL/auth/login"


# *-----------------ADMIN-----------------*
@app.route("/admin/races/close")
@check_auth
def close_race():
    return render_template("raceStopBetting.html")


@app.route("/admin/operations")
@check_auth
def admin_dashboard():
    return render_template("adminOperations.html")


@app.route("/admin/events/create")
@check_auth
def add_event():
    return render_template("eventAdd.html")


@app.route("/admin/event/races/manage")
@check_auth
def manage_race():
    return render_template("raceManage.html")


# *-----------------SELLERS-----------------*


@app.route("/ticket/info")
@check_auth
def update_ticket():
    # !adjust it here
    return render_template("cashier.html")


@app.route("/event/selection")
@check_auth
def event_selection():
    return render_template("eventSelection.html")


# lets choose event and race for ticket generation
@app.route("/ticket/purchase")
@check_auth
def ticket_purchase():
    return render_template("ticketPurchase.html")


if __name__ == "__main__":
    app.run(debug=True, port=5001)
