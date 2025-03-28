class Error(Exception):

    def __init__(self, msg="An error occurred", status_code=400):
        super().__init__(msg)
        self.message = msg
        self.status_code = status_code

    def format(self):
        return {"error": self.message}, self.status_code
