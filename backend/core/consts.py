MAX_LENGTH_CARD_NAME = 30
MAX_LENGTH_GROUP_NAME = 30
MAX_LENGTH_SHOP_NAME = 30
MAX_LENGTH_CARD_NUMBER = 40
MAX_LENGTH_BARCODE_NUMBER = 256
MAX_LENGTH_COLOR = 16
MAX_LENGTH_ENCODING_TYPE = 30
MAX_NUM_CARD_USE_BY_USER = None
FIELD_MASK = r"^[A-Za-zА-ЯЁа-яё\@\!\#\$\%\&\'\*\+\/\=\?\^\_\`\{\|\}\~\-\.\ ]+$"
FIELD_MASK_WITH_DIGITS = (
    r"^[A-Za-zА-ЯЁа-яё\d\@\!\#\$\%\&\'\*\+\/\=\?\^\_\`\{\|\}\~\-\.\ ]{1,30}$"
)
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
    CANNOT_SHARE_WITH_SELF = 'Вы не можете поделиться картой с самим собой.'
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
    INCORRECT_CARD_TITLE = (
        'Название может содержать только буквы, цифры, пробелы и спецсимволы.'
    )
    INCORRECT_EMAIL = 'Введен некорректный email'
    INCORRECT_SHOP_TITLE = (
        'Название может содержать только буквы, цифры, пробелы и спецсимволы.'
    )
    INCORRECT_PASSWORD = (
        'Пароль может содержать только латиницу и должен иметь хотя бы одну '
        'заглавную, одну строчную буквы и одну цифру. '
        'Минимальная длина - 8 знаков.'
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
    PASSWORD_TOO_LONG = 'Максимальная длина - 256 знаков.'
    PHONE_LAST_DIGITS_ARE_NOT_DIGITS = (
        'Здесь должны быть последние 4 цифры телефона.'
    )
    SERVER_ERROR = 'Ошибка сервера.'
    SUPERUSER_NOT_STAFF = 'У суперпользователя должно быть is_staff=True.'
    SUPERUSER_NOT_SUPERUSER = (
        'У суперпользователя должно быть is_superuser=True.'
    )
    TELEPHONE_NUMBER_INCORRECT = 'Номер телефона 10 цифр после +7.'
    TITLE_INCORRECT = (
        'Имя может содержать только буквы, цифры, пробелы и спецсимволы.'
    )
    TOO_SIMILAR_DATA = 'Пароль слишком похож на е-мейл.'

    def card_already_shared(self, email):
        return (
            f'У пользователя с е-мейл {email} '
            f'уже есть данная карта.'
        )


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
