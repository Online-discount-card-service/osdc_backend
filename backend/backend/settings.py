import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILES_DIR = os.path.join(BASE_DIR, 'data')
GROUP_FILES_DIR = os.path.join(DATA_FILES_DIR, 'group.csv')

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', default='some_secret_key')

DEBUG = os.getenv('DEBUG', default=False)

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    'backend',
    os.getenv('NGINX_HOST'),
]

CSRF_TRUSTED = os.getenv('CSRF_TRUSTED')
CSRF_TRUSTED_ORIGINS = [os.getenv('CSRF_TRUSTED_ORIGINS', default='http://localhost:8000')]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',
    'api',
    'core',
    'users.apps.UsersConfig',
    'drf_yasg',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', default='django.db.backends.sqlite3'),
        'NAME': os.getenv('DB_NAME', default=BASE_DIR / 'db.sqlite3'),
        'USER': os.getenv('POSTGRES_USER', default='user'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', default='password'),
        'HOST': os.getenv('DB_HOST', default='127.0.0.1'),
        'PORT': os.getenv('DB_PORT', default=5432)
    }
}

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'static/media')

AUTH_USER_MODEL = 'users.User'
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
    {
        'NAME': 'users.passwordvalidators.NumberValidator',
    },
    {
        'NAME': 'users.passwordvalidators.UppercaseValidator',
    },
    {
        'NAME': 'users.passwordvalidators.LowercaseValidator',
    },
    {
        'NAME': 'users.passwordvalidators.OnlyASCIIValidator',
    },
    {
        'NAME': 'users.passwordvalidators.MaximumLengthValidator',
    }
]

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'users.authentication.CustomTokenAuthentication',
    ],
    'EXCEPTION_HANDLER': 'api.exception_handler.custom_exception_handler',
}

DJOSER = {
    'LOGIN_FIELD': 'email',
    'SERIALIZERS': {
        'user_create': 'api.serializers.CustomUserCreateSerializer',
        'user': 'api.serializers.UserReadSerializer',
        'current_user': 'api.serializers.UserReadSerializer',
        'token_create': 'api.serializers.CustomTokenCreateSerializer',
        'password_reset': 'api.serializers.CustomSendEmailResetPasswordSerializer',
        'activation': 'api.serializers.CustomActivationSerializer',
    },
    'EMAIL': {
        'activation': 'api.email.CustomActivationEmail',
        'password_reset': 'api.email.CustomPasswordResetEmail'
    },
    'PERMISSIONS': {
        'user': ['djoser.permissions.CurrentUserOrAdmin'],
        'activation': ['api.permissions.IsUserEmailOwner'],
    },
    'HIDE_USERS': True,
    'SEND_ACTIVATION_EMAIL': True,
    'ACTIVATION_URL': 'activate/{uid}/{token}',
    'PASSWORD_RESET_CONFIRM_URL': 'password_reset_confirm/{uid}/{token}',
}

# SendGrid settings
EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"
DEFAULT_FROM_EMAIL = os.getenv('SENDGRID_FROM_EMAIL')
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
SENDGRID_SANDBOX_MODE_IN_DEBUG = False

if os.getenv('EMAIL_DEBUG', default=False):
    EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
    EMAIL_FILE_PATH = os.path.join(STATIC_ROOT, 'sent_emails')

# TODO убрать на продакшене
CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
    'http://127.0.0.1:5173',
]
