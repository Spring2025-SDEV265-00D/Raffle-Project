from flask import Flask, render_template

app = Flask(__name__)

#home page, nothing here yet
@app.route('/')
def home():
    return render_template('index.html')

#check ticker status with reference_number
@app.route('/ticket/status')
def ticket_status():
    return render_template('ticketStatus.html')

#lets choose event and race for ticket generation
@app.route('/ticket/purchase')
def ticket_purchase():
    return render_template('ticketPurchase.html')



if __name__ == '__main__':
    app.run(debug=True, port=5001)
