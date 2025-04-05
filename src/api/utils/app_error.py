import inspect


class AppError(Exception):

    def __init__(self, msg="An error occurred", status_code=400, context=None):
        super().__init__(msg)
        self.message = msg
        self.status_code = status_code
        self.context = context

    @staticmethod
    def format(error) -> tuple[dict, int]:

        response = {"error": error.message}
        if error.context:
            response["context"] = error.context
        return response, error.status_code

    @staticmethod
    def get_error_context(**kwargs):
        frame = inspect.currentframe().f_back
        context = {
            "function": frame.f_code.co_name,
            "file": frame.f_code.co_filename,
            "line": frame.f_lineno,
        }
        context.update(kwargs)
        return context


class NotFoundError(AppError):
    def __init__(self, msg, status_code=500, context=None):

        msg = f"Not found: {msg}"

        super().__init__(msg, status_code, context)


class EmptyDataError(AppError):
    """Base error for valid requests with empty results."""

    def __init__(self, msg, status_code=500, context=None):
        msg = f"Empty data: {msg}"

        super().__init__(msg, status_code, context)


class DatabaseError(AppError):
    """Base error for failed database operations(updates, inserts, etc.)."""

    def __init__(self, msg, status_code=500, context=None):
        msg = f"Failed database operation: {msg}"

        super().__init__(msg, status_code, context)


class ModelStateError(AppError):
    """Base error for request already fulfiled"""

# adjust status code for this
# front end must handle these codes..
    def __init__(self, msg, status_code=400, context=None):
        msg = f"Model State Error: {msg}"

        super().__init__(msg, status_code, context)


class PayloadError(AppError):
    """Base error for mismatch in request payload """

# adjust status code for this
# front end must handle these codes..
    def __init__(self, msg, status_code=400, context=None):
        msg = f"Payload Error: {msg}"

        super().__init__(msg, status_code, context)
