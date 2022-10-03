from dotenv import load_dotenv
from pathlib import Path
import dj_database_url
import os

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')

IS_HEROKU = 'DYNO' in os.environ

if IS_HEROKU:
    DEBUG = False
else:
    DEBUG = os.getenv('DEBUG')

if IS_HEROKU:
    ALLOWED_HOSTS = ['*']
else:
    ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost').split(',')

AUTH_USER_MODEL = 'user.User'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_filters',
    'jwt_auth',
    'user',
    'blog'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'jwt_auth.middleware.JWTMiddleware'
]

ROOT_URLCONF = 'InnotterDjango.urls'

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

WSGI_APPLICATION = 'InnotterDjango.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': os.getenv('POSTGRES_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.getenv('POSTGRES_DB', 'innotter_db'),
        'HOST': os.getenv('POSTGRES_HOST'),
        'PORT': os.getenv('POSTGRES_PORT'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'CONN_MAX_AGE': int(os.getenv('CONN_MAX_AGE', '0'))
    }
}

if "DATABASE_URL" in os.environ:
    DATABASES["default"] = dj_database_url.config(
        conn_max_age=int(os.getenv('CONN_MAX_AGE', '0')),
        ssl_require=True
    )

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'UserAttributeSimilarityValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'MinimumLengthValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'CommonPasswordValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'NumericPasswordValidator'
            ),
    },
]

JWT_TOKEN = {
    'ACCESS_TOKEN_LIFETIME_MINUTES': 15,
    'REFRESH_TOKEN_LIFETIME_DAYS': 30,
    'ALGORITHMS': ['HS256'],
    'SECURE': True,
    'HTTP_ONLY': True,
}

LANGUAGE_CODE = 'en-us'

USE_I18N = True

USE_L18N = True

TIME_ZONE = 'UTC'

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --------------------------- RabbitMQ Configuration --------------------------

RABBITMQ = {
    'PROTOCOL': os.getenv('RABBITMQ_PROTOCOL'),
    'HOST': os.getenv('RABBITMQ_HOST'),
    'PORT': os.getenv('RABBITMQ_PORT'),
    'USER': os.getenv('RABBITMQ_USER'),
    'PASSWORD': os.getenv('RABBITMQ_PASSWORD'),
}

CELERY_BROKER_URL = CELERY_BROKER_URL = (
    f"{RABBITMQ['PROTOCOL']}://{RABBITMQ['USER']}:"
    f"{RABBITMQ['PASSWORD']}@{RABBITMQ['HOST']}:{RABBITMQ['PORT']}"
)

CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}

# -------------------------- AWS Configuration --------------------------------

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION_NAME = os.getenv('AWS_REGION_NAME')
AWS_MAIL_SENDER = os.getenv('AWS_MAIL_SENDER')
AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')
