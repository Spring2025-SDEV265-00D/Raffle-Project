from flask import Flask, render_template
from dotenv import load_dotenv
import os
import requests
# from auth import check_auth, check_role

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
    return render_template("login.html")


# *-----------------ADMIN-----------------*
@app.route("/admin/races/close")
# @check_auth
# @check_role('Admin')
def close_race():
    return render_template("raceStopBetting.html")


@app.route("/admin/operations")
# @check_auth
# @check_role('Admin')
def admin_dashboard():
    try:
        response = requests.get(f"{API_BASE_URL}/fetch/events")
        response.raise_for_status()
        events = response.json()
    except Exception as e:
        events = []
        print(f"Error fetching events: {e}")

    return render_template("adminOperations.html", events=events)


@app.route("/admin/events/create")
# @check_auth
# @check_role('Admin')
def add_event():
    return render_template("eventAdd.html")


@app.route("/admin/event/races/manage")
# @check_auth
# @check_role('Admin')
def manage_race():
    return render_template("raceManage.html")

@app.route("/admin/race/horses/manage")
# @check_auth
# @check_role('Admin')
def manage_horses():
    return render_template("manageHorses.html")

# *-----------------SELLERS-----------------*


@app.route("/ticket/info")
# @check_auth
# @check_role('Cashier')
def update_ticket():
    return render_template("cashier.html")


@app.route("/event/selection")
# @check_auth
# @check_role('Seller')
def event_selection():
    return render_template("eventSelection.html")


# lets choose event and race for ticket generation
@app.route("/ticket/purchase")
# @check_auth
# @check_role('Seller')
def ticket_purchase():
    return render_template("ticketPurchase.html")


if __name__ == "__main__":
    app.run(debug=True, port=5001)
