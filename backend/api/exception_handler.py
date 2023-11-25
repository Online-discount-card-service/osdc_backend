from rest_framework.exceptions import APIException
from rest_framework.response import Response


ERROR_MESSAGES = {
    400: 'Введены некорректные данные.',
    401: 'Ошибка авторизации.',
    403: 'Ошибка авторизации.',
    404: 'Нет данных.',
    405: 'Действие запрещено.',
    408: 'Таймаут.',
    413: 'Слишком большой запрос.',
    414: 'Слишком длинный URI',
    415: 'Неподдерживаемый тип данных.',
    429: 'Слишком много запросов.',
    431: 'Заголовок слишком большой.',
}


def custom_exception_handler(exc: APIException, context):
    """
    Пользовательский обработчик исключений.

    :param exc: Исключение.
    :param context: Контекст запроса.
    :return: Ответ API.
    """

    response_data = {'detail': getattr(exc, 'detail', None)}
    response = Response(response_data, status=exc.status_code)

    if exc.status_code in ERROR_MESSAGES:
        response.data['message'] = ERROR_MESSAGES.get(exc.status_code)
    elif 500 <= exc.status_code <= 599:
        response.data['Message'] = 'Ошибка сервера.'
    else:
        response.data['Message'] = 'Что-то пошло не так.'

    return response
