from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        response.data["message"] = response.data["detail"]

    return response


class CustomApiException(APIException):

    message = None
    status_code = None

    def __init__(self, message, status_code):
        CustomApiException.status_code = status_code
        CustomApiException.message = message


class CustomNotFound(CustomApiException):

    status_code = 404
    message = None

    def __init__(self, message="Not Found"):
        CustomNotFound.detail = message


class CustomUnableToCreateError(CustomApiException):

    status_code = 422
    message = None

    def __init__(self, message="An Error Occurred While Creating The Object !"):
        CustomUnableToCreateError.detail = message


class CustomServerError(CustomApiException):

    status_code = 500
    message = None

    def __init__(self, message="Not Found"):
        CustomNotFound.detail = message
