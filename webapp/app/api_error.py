# Super simple Flask exception class
# http://flask.pocoo.org/docs/0.10/patterns/apierrors/
class ApiError(Exception):
    def __init__(self, message, status_code=400, cause=None):
        Exception.__init__(self)

        self.message = message
        if status_code is not None:
            self.status_code = status_code

        self.cause = cause

    def to_dict(self):
        return {
            "message": "{0} {1}".format(self.message, "Cause: {0}".format(repr(self.cause)) if self.cause else "")
        }
