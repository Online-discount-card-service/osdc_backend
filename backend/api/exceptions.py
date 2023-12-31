from rest_framework import exceptions, status

from core.consts import ErrorMessage


class StatisticsError(exceptions.APIException):
    """В запросе передано число меньше, чем уже записано в статистике."""

    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = {
        'usage_number': ErrorMessage.INCORRECT_USAGE_STATISTICS
    }
