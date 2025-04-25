from flask import abort
from functools import wraps  # keeps function properties instead of wrapper's
from flask import request
from .util import Util
from .app_error import PayloadError


def validate_payload_structure(expected_fields=None, expected_headers=None, expected_nested=None, expecting_payload=True):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):

            # *Insufficient arguments  fallback
            if not expected_headers and not expected_fields and expecting_payload:
                raise PayloadError(  # need context?
                    "No expected incoming data structure provided: either `expected_fields` or `expected_headers` are required.")

            # REQUEST CASES
            # * Handled by CORS
            if request.method == "OPTIONS":
                return func(*args, **kwargs)

            # needs to be more robust if using other methods besides POST and GET
            # todo: request.method in ("POST", "PUT", "PATCH", "DELETE"):
            # *Handles both types of request, extracting data accordingly

            payload = request.args.to_dict() if request.method == "GET" else request.get_json()
           # payload = request.get_json() if request.method in (
           #     "POST", "PATCH") else request.args.to_dict()

            # Util.p("in decorator payload", payload=payload)

            # *Support for no-payload routes, ensures nothing incoming
            if not expecting_payload:
                if payload:
                    raise PayloadError(
                        "Expecting no data, but request body is not empty.", context=PayloadError.get_error_context(payload=payload))

                kwargs["validated_payload"] = None
                return func(*args, **kwargs)

            # Cases for nested and flat
            if expected_headers:  # *Validate hearders and nested
                validated = Util.valid_nested_payload(
                    payload=payload,
                    expected_headers=expected_headers,
                    expected_nested=expected_nested
                )
            elif expected_fields:  # * Validate flat otherwise

                validated = Util.valid_payload(
                    payload=payload,
                    expected=expected_fields
                )

            # Util.p("in decorator", validated=validated)

            # *what is actually being passed on to the route
            kwargs["validated_payload"] = validated
            return func(*args, **kwargs)
        return wrapper
    return decorator
