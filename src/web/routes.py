from flask import Flask, render_template
from dotenv import load_dotenv

import os

load_dotenv()
API_BASE_URL = os.getenv("API_BASE_URL")
app = Flask(__name__)


# This will add the API_BASE_URL to the context of the app,
# so that all of the templates can access it.
@app.context_processor
def inject_globals():
    return dict(api_base_url=API_BASE_URL)


# *-----------------ADMIN-----------------*
@app.route("/admin/races/close")
def close_race():
    return render_template("raceStopBetting.html")


@app.route("/admin/operations")
def admin_dashboard():
    return render_template("adminOperations.html")


@app.route("/admin/events/create")
def add_event():
    return render_template("eventAdd.html")


@app.route("/admin/event/races/manage")
def manage_race():
    return render_template("raceManage.html")


# *-----------------SELLERS-----------------*


@app.route("/ticket/info")
def update_ticket():
    # !adjust it here
    return render_template("cashier.html")


# home page, nothing here yet
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/event/selection")
def event_selection():
    return render_template("eventSelection.html")


# lets choose event and race for ticket generation
@app.route("/ticket/purchase")
def ticket_purchase():
    return render_template("ticketPurchase.html")


if __name__ == "__main__":
    app.run(debug=True, port=5001)
