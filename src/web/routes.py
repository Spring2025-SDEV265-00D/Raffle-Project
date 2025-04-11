from flask import Flask, render_template

app = Flask(__name__)


@app.route("/test")
def test():
    return render_template("testing.html")


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

# @app.route("/ticket/info", methods=["GET"])
@app.route("/ticket/info")
def update_ticket():
    return render_template("cashier.html")  # !adjust it here


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


@app.route("/ticket/status")
def ticket_status():
    return render_template("ticketStatus.html")


@app.route("/ticket/cancel")
def ticket_cancel():
    return render_template("ticketCancel.html")


if __name__ == "__main__":
    app.run(debug=True, port=5001)
