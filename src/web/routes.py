from flask import Flask, render_template, request, redirect, url_for, flash, session
from dotenv import load_dotenv
import os
from auth import check_auth, check_role
import requests
# from auth import check_auth, check_role

load_dotenv()
API_BASE_URL = os.getenv("API_BASE_URL")

app = Flask(__name__)
# Set a default secret key if not found in environment
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret-key-please-change-in-production")


# This will add the API_BASE_URL and user info to the context of the app,
# so that all of the templates can access it.
@app.context_processor
def inject_globals():
    # Only fetch user info if we have a session but no user info
    if session.get('session') and not session.get('user_info'):
        try:
            response = requests.get(
                f"{API_BASE_URL}/auth/me",
                headers={'Cookie': f'session={session.get("session")}'}
            )
            if response.status_code == 200:
                session['user_info'] = response.json()
        except Exception as e:
            print(f"Error fetching user info: {str(e)}")
    
    return dict(
        api_base_url=API_BASE_URL,
        user_info=session.get('user_info')
    )


# *-----------------LOGIN-----------------*
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get form data
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Make request to API for authentication
        try:
            response = requests.post(
                f"{API_BASE_URL}/auth/login",
                data={"username": username, "password": password}
            )
            
            if response.status_code == 200:
                response_data = response.json()
                # Store the session cookie
                session_cookie = response.cookies.get('session')
                if session_cookie and response_data.get('status') == 'success':
                    # Clear any existing session data
                    session.clear()
                    # Set new session data
                    session['session'] = session_cookie
                    session['user_info'] = response_data
                    
                    # Get role from login response
                    role = response_data.get('role', {}).get('role')
                    
                    # Redirect based on role
                    if role == 'Admin':
                        return redirect(url_for('admin_dashboard'))
                    elif role == 'Seller':
                        return redirect(url_for('event_selection'))
                    elif role == 'Cashier':
                        return redirect(url_for('update_ticket'))
                    
                    # Default redirect if role check fails
                    return redirect(url_for('admin_dashboard'))
            
            flash('Invalid username or password')
        except Exception as e:
            flash('An error occurred during login')
            print(f"Login error: {str(e)}")
    
    return render_template('login.html')


# *-----------------ADMIN-----------------*
@app.route("/admin/races/close")
@check_auth
@check_role('Admin')
def close_race():
    return render_template("raceStopBetting.html")


@app.route("/admin/operations")
@check_auth
@check_role('Admin')
def admin_dashboard():
    return render_template("adminOperations.html")


@app.route("/admin/events/create")
@check_auth
@check_role('Admin')
def add_event():
    return render_template("eventAdd.html")


@app.route("/admin/event/races/manage")
@check_auth
@check_role('Admin')
def manage_race():
    return render_template("raceManage.html")


@app.route("/admin/users/register", methods=['GET', 'POST'])
@check_auth
@check_role('Admin')
def register_user_page():
    if request.method == 'POST':
        try:
            # Forward the request to the API
            response = requests.post(
                f"{API_BASE_URL}/auth/register",
                data=request.form,
                headers={'Cookie': f'session={session.get("session")}'}
            )
            
            if response.status_code == 201:
                flash('User registered successfully!', 'success')
                return redirect(url_for('admin_dashboard'))
            else:
                flash(response.json().get('message', 'Error registering user'), 'error')
        except Exception as e:
            flash('An error occurred during registration', 'error')
            print(f"Registration error: {str(e)}")
    
    return render_template("userRegistration.html")


# *-----------------SELLERS-----------------*


@app.route("/ticket/info")
@check_auth
@check_role('Cashier')
def update_ticket():
    return render_template("cashier.html")


@app.route("/event/selection")
@check_auth
@check_role('Seller')
def event_selection():
    return render_template("eventSelection.html")


# lets choose event and race for ticket generation
@app.route("/ticket/purchase")
@check_auth
@check_role('Seller')
def ticket_purchase():
    return render_template("ticketPurchase.html")


@app.route("/logout")
def logout():
    # Clear the session
    session.clear()
    # Redirect to login page
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True, port=5001)
