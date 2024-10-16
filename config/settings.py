"""
Django settings for django_template_42_project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import json, logging, os
import pathlib
from dotenv import load_dotenv, find_dotenv


## load envars ------------------------------------------------------
dotenv_path = pathlib.Path(__file__).resolve().parent.parent.parent / '.env'
assert dotenv_path.exists(), f'file does not exist, ``{dotenv_path}``'
load_dotenv( 
    find_dotenv( str(dotenv_path), raise_error_if_not_found=True ), 
    override=True 
    )


log = logging.getLogger(__name__)


## django project settings ------------------------------------------

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
# log.debug( f'BASE_DIR, ``{BASE_DIR}``' )


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-3ory+ty87_wq8-21ki6d&a+x=z9_$2m(gr4@vxri@@^g7u!*oc'
SECRET_KEY = os.environ[ 'SECRET_KEY' ]

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
DEBUG = json.loads( os.environ['DEBUG_JSON'] )

ADMINS = json.loads( os.environ['ADMINS_JSON'] )

ALLOWED_HOSTS = json.loads( os.environ['ALLOWED_HOSTS_JSON'] )
CSRF_TRUSTED_ORIGINS = json.loads( os.environ['CSRF_TRUSTED_ORIGINS_JSON'] )    

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 'DIRS': [ '%s/foo_app' % BASE_DIR ],
        'DIRS': [ f'{BASE_DIR}/foo_app/foo_app_templates' ],
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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = json.loads( os.environ['DATABASES_JSON'] )

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'  ## the default
TIME_ZONE = 'America/New_York'

USE_I18N = True

# USE_TZ = True  ## the default
USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = os.environ['STATIC_URL']
STATIC_ROOT = os.environ['STATIC_ROOT']  # needed for collectstatic command

# Email
SERVER_EMAIL = os.environ['SERVER_EMAIL']
EMAIL_HOST = os.environ['EMAIL_HOST']
EMAIL_PORT = int( os.environ['EMAIL_PORT'] )


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

## reminder: 
## "Each 'logger' will pass messages above its log-level to its associated 'handlers', 
## ...which will then output messages above the handler's own log-level."
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': "[%(asctime)s] %(levelname)s [%(module)s-%(funcName)s()::%(lineno)d] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
        'logfile': {
            'level': os.environ.get( 'LOG_LEVEL', 'INFO' ),  # add LOG_LEVEL=DEBUG to the .env file to see debug messages
            'class':'logging.FileHandler',  # note: configure server to use system's log-rotate to avoid permissions issues
            'filename': os.environ['LOG_PATH'],
            'formatter': 'standard',
        },
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'foo_app': {
            'handlers': ['logfile'],
            'level': 'DEBUG',  # messages above this will get sent to the `logfile` handler
            'propagate': False
        },
        # 'django.db.backends': {  # re-enable to check sql-queries! <https://docs.djangoproject.com/en/4.2/ref/logging/#django-db-backends>
        #     'handlers': ['logfile'],
        #     'level': os.environ['LOG_LEVEL'],
        #     'propagate': False
        # },
    }
}
