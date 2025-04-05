from flask import Flask, render_template

app = Flask(__name__)


# *-----------------ADMIN-----------------*
@app.route("/admin/races/close")
def close_race():
    return render_template("raceStopBetting.html")


# *-----------------SELLERS-----------------*


# home page, nothing here yet
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/test")
def test():
    return render_template("ticketPurchaseTEST.html")


@app.route("/event/selection")
def event_selection():
    return render_template("eventSelection.html")


# check ticker status with reference_number
@app.route("/ticket/status")
def ticket_status():
    return render_template("ticketStatus.html")


# lets choose event and race for ticket generation
@app.route("/ticket/purchase")
def ticket_purchase():
    return render_template("ticketPurchase.html")


@app.route("/ticket/cancel")
def ticket_cancel():
    return render_template("ticketCancel.html")


if __name__ == "__main__":
    app.run(debug=True, port=5001)
