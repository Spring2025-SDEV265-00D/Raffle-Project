from functools import wraps
from flask import redirect, url_for, request, session
import requests
from dotenv import load_dotenv
import os

load_dotenv()
API_BASE_URL = os.getenv("API_BASE_URL")

def check_auth(f):
    """
    Decorator that checks if the user is authenticated.
    When used, this will run before the route handler is executed.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get the session cookie from the API if it exists
        session_cookie = session.get('session')

        if not session_cookie:
            return redirect(url_for('login'))

        # Verify with API if the session is valid
        headers = {'Cookie': f'session={session_cookie}'}
        response = requests.get(f"{API_BASE_URL}/auth/me", headers=headers)

        if response.status_code != 200:
            session.clear()
            return redirect(url_for('login'))

        return f(*args, **kwargs)

    return decorated_function

def check_role(allowed_roles: str | list[str]):
    """
    Decorator that checks if the user has the required role(s).
    Must be used after @check_auth to ensure user is authenticated.
    """
    if isinstance(allowed_roles, str):
        allowed_roles = [allowed_roles]

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Get the session cookie from the API if it exists
            session_cookie = session.get('session')

            # Verify role with API
            headers = {'Cookie': f'session={session_cookie}'}
            response = requests.get(f"{API_BASE_URL}/auth/me", headers=headers)

            if response.status_code != 200:
                session.clear()
                return redirect(url_for('login'))

            user_role = response.json()['role']['role']
            if user_role != 'Admin' and user_role not in allowed_roles:
                return "Access forbidden: Insufficient role", 403

            return f(*args, **kwargs)

        return decorated_function

    return decorator
