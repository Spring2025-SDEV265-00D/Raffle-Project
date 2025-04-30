from functools import wraps
from flask import redirect, url_for, request
import requests
from dotenv import load_dotenv
import os

load_dotenv()
API_BASE_URL = os.getenv("API_BASE_URL")


## When used, this will run before the route handler is executed.
def check_auth(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get the session cookie from the API if it exists
        api_session_cookie = request.cookies.get('session')

        if not api_session_cookie:
            return redirect(url_for('login'))

        # Verify with API if the session is valid
        headers = {'Cookie': f'session={api_session_cookie}'}
        response = requests.get(f"{API_BASE_URL}/auth/me", headers=headers)

        if response.status_code != 200:
            return redirect(url_for('login'))

        return f(*args, **kwargs)

    return decorated_function
