import os
from datetime import timedelta

import dotenv
import logging.config
from pathlib import Path

# Настройка окружения
BASE_DIR = Path(__file__).resolve().parent.parent

dotenv_file = os.path.join(BASE_DIR.parent, ".env.back")

if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

# Базовые настройки приложения
SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = os.getenv('DEBUG')

PRODUCTION = os.getenv('PRODUCTION')

ROOT_URLCONF = 'Config.urls'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(' ')

LOGGING_CONFIG = None

LOGLEVEL = os.getenv('DJANGO_LOGLEVEL').upper()

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(asctime)s %(levelname)s [%(name)s:%(lineno)s] %(module)s %(process)d %(thread)d %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console',
        },
    },
    'loggers': {
        '': {
            'level': LOGLEVEL,
            'handlers': ['console', ],
        },
    },
})

# Настройки языка и времени
LANGUAGE_CODE = os.getenv('LANGUAGE_CODE')

TIME_ZONE = os.getenv('TIME_ZONE')

USE_I18N = os.getenv('USE_I18N')

USE_L10N = os.getenv('USE_L10N')

USE_TZ = os.getenv('USE_TZ')

# Базовые настройки базы данных
DB_USER = os.getenv('DB_USER')

DB_USER_PASSWORD = os.getenv('DB_USER_PASSWORD')

DB_HOST = os.getenv('DB_HOST')

DB_NAME = os.getenv('DB_NAME')

DB_PORT = os.getenv('DB_PORT')

CONN_MAX_AGE = None

# # Базовые настройки Celery
# RABBITMQ_DEFAULT_USER=os.getenv('RABBITMQ_DEFAULT_USER')
#
# RABBITMQ_DEFAULT_PASS=os.getenv('RABBITMQ_DEFAULT_PASS')
#
# CELERY_BROKER_URL= f'amqp://{RABBITMQ_DEFAULT_USER}:{RABBITMQ_DEFAULT_PASS}@rabbit:5672/'
#
# CELERY_ACCEPT_CONTENT = os.getenv('CELERY_ACCEPT_CONTENT').split(' ')
#
# CELERY_TASK_SERIALIZER = os.getenv('CELERY_TASK_SERIALIZER')
#
# CELERY_RESULT_SERIALIZER = os.getenv('CELERY_RESULT_SERIALIZER')
#
# CELERYD_PREFETCH_MULTIPLIER = os.getenv('CELERYD_PREFETCH_MULTIPLIER')
#
# CELERY_TIMEZONE = os.getenv('CELERY_TIMEZONE')
#
# CELERY_CACHE_BACKEND = os.getenv('CELERY_CACHE_BACKEND')
#
# CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND')
#
# CELERY_CREATE_MISSING_QUEUES = os.getenv('CELERY_CREATE_MISSING_QUEUES')
#
# CELERYD_MAX_TASKS_PER_CHILD = os.getenv('CELERYD_MAX_TASKS_PER_CHILD')
#
# CELERY_BROKER_CONNECTION_RETRY = os.getenv('CELERY_BROKER_CONNECTION_RETRY')
#
# CELERY_DISABLE_RATE_LIMITS = os.getenv('CELERY_DISABLE_RATE_LIMITS')
#
# CELERY_BROKER_CONNECTION_MAX_RETRIES = os.getenv('CELERY_BROKER_CONNECTION_MAX_RETRIES')

# Настройки аккаунта админитратора
ADMINS = [
    {
        'first_name': os.getenv('ADMIN_FIRST_NAME'),
        'last_name': os.getenv('ADMIN_LAST_NAME'),
        'gender': os.getenv('ADMIN_GENDER'),
        'email': os.getenv('ADMIN_EMAIL'),
        'password': os.getenv('ADMIN_PASSWORD'),
    }
]

# Установленные приложения
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'api',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'rest_framework',
    'djoser',
    # 'django_celery_beat',
    # 'django_celery_results',
    # 'djcelery_email',
    # 'django_prometheus',
    'corsheaders',
]

# Промежуточные слои
MIDDLEWARE = [
    # 'django_prometheus.middleware.PrometheusBeforeMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    # 'django_prometheus.middleware.PrometheusAfterMiddleware',
]

# Настройки шаблонизатора
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # 'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

TEMPLATE_LOADERS = [
    # Loads templates from DIRS setting:
    'django.template.loaders.filesystem.Loader',

    # Loads templates from your installed apps:
    'django.template.loaders.app_directories.Loader',
]

# Настройка запуска приложения
ASGI_APPLICATION = 'Config.asgi.application'
# WSGI_APPLICATION = 'Config.wsgi.application'

# Настройка базы данных
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_USER_PASSWORD,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
    }
}

# # Настройка кэша
# CACHES = {
#     'default': {
#         'BACKEND': 'django_prometheus.cache.backends.filebased.FileBasedCache',
#         'LOCATION': '/var/tmp/django_cache',
#     },  # Мониторинг кэша с помощью Prometheus
# }

# Настройка медиафайлов и статики
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATIC_URL = '/static/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "media")

# Переопределение стандартного пользователя
AUTH_USER_MODEL = 'api.User'

# Настройки CORS заголовков
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

# Настройки DRF
REST_FRAMEWORK = {
    # Права доступа поумолчанию
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
    ],
    # Тип токенов и авторизации
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication"
    ],
}

# Настройки Djoser
DJOSER = {
    'PASSWORD_RESET_CONFIRM_URL': 'home/reset_password/{uid}/{token}#reset_password_confirmation',
    'ACTIVATION_URL': 'home/activation/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': True,
    'SEND_CONFIRMATION_EMAIL': True,
    'TOKEN_MODEL': None,
    'HIDE_USERS': True,
    'SERIALIZERS': {},
    'PERMISSIONS': {
        'activation': ['rest_framework.permissions.AllowAny'],
        'password_reset': ['rest_framework.permissions.AllowAny'],
        'password_reset_confirm': ['rest_framework.permissions.AllowAny'],
        'set_password': ['djoser.permissions.CurrentUserOrAdmin'],
        'username_reset': ['rest_framework.permissions.AllowAny'],
        'username_reset_confirm': ['rest_framework.permissions.AllowAny'],
        'set_username': ['djoser.permissions.CurrentUserOrAdmin'],
        'user_create': ['rest_framework.permissions.AllowAny'],
        'user_delete': ['djoser.permissions.CurrentUserOrAdmin'],
        'user': ['djoser.permissions.CurrentUserOrAdmin'],
        'user_list': ['djoser.permissions.CurrentUserOrAdmin'],
        'token_create': ['rest_framework.permissions.AllowAny'],
        'token_destroy': ['rest_framework.permissions.IsAuthenticated'],
    }
}

# Настройки JWT
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=2),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=5),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('JWT',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(days=2),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=5),
}

# Директория файлов заполнения базы данных из JSON
FIXTURE_DIRS = [
    '/fixtures/'
]

# Настройки почты
# EMAIL_BACKEND = 'djcelery_email.backends.CeleryEmailBackend'
#
# CELERY_EMAIL_TASK_CONFIG = {
#     'queue': 'email',
#     'rate_limit': '50/m',  # * CELERY_EMAIL_CHUNK_SIZE (default: 10)
# }

EMAIL_HOST = os.environ.get('EMAIL_HOST')

EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')

EMAIL_USE_TLS = True

DEFAULT_FROM_EMAIL = os.environ.get('EMAIL_HOST_USER')

EMAIL_PORT = os.environ.get('EMAIL_PORT')

EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
