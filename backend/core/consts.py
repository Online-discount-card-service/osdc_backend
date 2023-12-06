MAX_LENGTH_CARD_NAME = 30
MAX_LENGTH_GROUP_NAME = 20
MAX_LENGTH_SHOP_NAME = 30
MAX_LENGTH_CARD_NUMBER = 40
MAX_LENGTH_COLOR = 16
MAX_LENGTH_ENCODING_TYPE = 30
MAX_NUM_CARD_USE_BY_USER = None
CODE128 = 'code128'
CODE39 = 'code39'
UPC_A = 'upc-a'
UPC_E = 'upc-e'
EAN_13 = 'ean-13'
EAN_8 = 'ean-8'
QR_код = 'qr-kod'
ENCODING_TYPE = (
    (CODE128, 'CODE128'),
    (CODE39, 'CODE39'),
    (UPC_A, 'UPC-A'),
    (UPC_E, 'UPC-E'),
    (EAN_13, 'EAN-13'),
    (EAN_8, 'EAN-8'),
    (QR_код, 'QR-код'),
)


class ErrorMessage:
    STATUS_ERROR_MESSAGES = {
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
    CARD_HAS_NO_BARCODE_OR_NUMBER = (
        'Необходимо указать номер карты и/или штрих-кода.'
    )
    CARD_STATUS_AS_REQUESTED = 'Статус карты уже соответствует запрашиваемому.'
    EMAIL_ALREADY_ACTIVATED = 'Почта уже подтверждена.'
    GENERAL_ERROR = 'Что-то пошло не так.'
    INCORRECT_BARCODE = (
        'Номер штрих-кода может содержать только буквы, цифры, пробелы, '
        'тире и нижнее подчеркивание.'
    )
    INCORRECT_CARD_NUMBER = (
        'Номер карты может содержать только буквы, цифры, пробелы, '
        'тире и нижнее подчеркивание.'
    )
    INCORRECT_COLOR_FORMAT = (
        'Неверный формат для цвета, должно быть #AABBCC или #ABC.'
    )
    INCORRECT_TITLE = (
        'Название может содержать только буквы, цифры, пробелы и спецсимволы.'
    )
    INCORRECT_UID = 'Неверный формат uid.'
    INCORRECT_USAGE_STATISTICS = (
        'Счётчик использования можно только увеличить!'
    )
    INCORRECT_USERS_DATA = 'Неверные данные пользователя.'
    INVALID_CREDENTIALS = 'Неверные учетные данные.'
    MUST_HAVE = 'Обязательное поле.'
    NAME_INCORRECT = 'Имя может содержать только буквы, пробелы и спецсимволы.'
    NO_EMAIL_ON_USER_CREATION = 'Электронная почта должна быть установлена.'
    NONUNIQUE_EMAIL = 'Пользователь с таким email уже существует.'
    PASSWORD_NO_LOWER_CASE = (
        'Пароль должен содержать как минимум одну маленькую букву, '
        'a-z или а-я.'
    )
    PASSWORD_NO_NUMBERS = (
        'Пароль должен содержать как минимум одну цифру, 0-9.'
    )
    PASSWORD_NO_UPPER_CASE = (
        'Пароль должен содержать как минимум одну большую букву, A-Z или А-Я.'
    )
    PHONE_LAST_DIGITS_ARE_NOT_DIGITS = (
        'Здесь должны быть последние 4 цифры телефона.'
    )
    SERVER_ERROR = 'Ошибка сервера.'
    SUPERUSER_NOT_STAFF = 'У суперпользователя должно быть is_staff=True.'
    SUPERUSER_NOT_SUPERUSER = (
        'У суперпользователя должно быть is_superuser=True.'
    )
    TELEPHONE_NUMBER_INCORRECT = 'Номер телефона 10 цифр после +7.'
    TOO_SIMILAR_DATA = 'Пароль слишком похож на е-мейл.'


class Message:
    CARD_DELETION_SUCCESS = 'Карта успешно удалена.'
    LOGOUT_SUCCESS = 'Вы успешно вышли из учетной записи.'

    def invitation_message_create(self, email):
        return (
            f'Пользователя с таким емейл ({email}) нет, '
            f'но мы направили ему приглашение.'
        )

    def successful_sharing(self, email):
        return (
            f'Вы успешно поделились картой '
            f'с пользователем, чья почта {email}!'
        )
