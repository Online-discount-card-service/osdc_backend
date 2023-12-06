from django.core.exceptions import PermissionDenied
from django.http import Http404
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.views import exception_handler

from core.consts import ErrorMessage


def handle_api_exception(exc, response):
    def process_errors(errors, parent_key=None, response_data=None):
        if response_data is None:
            response_data = {'detail': {}}

        for field, value in errors.items():
            current_key = f'{parent_key}_{field}' if parent_key else field
            if isinstance(value, dict):
                process_errors(value, current_key, response_data)
            else:
                response_data['detail'][current_key] = value

        return response_data

    response_data = {'detail': getattr(exc, 'detail', None)}
    response = Response(
        response_data,
        status=exc.status_code,
        headers=response.headers
    )

    if exc.status_code in ErrorMessage.ERROR_MESSAGES:
        response.data['message'] = ErrorMessage.ERROR_MESSAGES.get(
            exc.status_code
        )
    elif 500 <= exc.status_code <= 599:
        response.data['message'] = ErrorMessage.SERVER_ERROR
    else:
        response.data['message'] = ErrorMessage.GENERAL_ERROR

    if exc.status_code == 400:
        fields_errors = response.data.pop('detail')
        if isinstance(fields_errors, dict):
            response.data.update(process_errors(fields_errors))
        else:
            response.data['detail'] = {"non_field_errors": fields_errors}
    return response


def custom_exception_handler(exc, context):
    """Обработчик исключений для фронта."""

    response = exception_handler(exc, context)

    if isinstance(exc, Http404):
        exc = exceptions.NotFound()
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    if isinstance(exc, exceptions.APIException):
        response = handle_api_exception(exc, response)

    return response
