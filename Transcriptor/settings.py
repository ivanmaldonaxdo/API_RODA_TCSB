"""
Django settings for Transcriptor project.

Generated by 'django-admin startproject' using Django 3.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
from audioop import reverse
import datetime
from pathlib import Path
import os
from django.urls import reverse_lazy
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-82e32v=_md3-ydr+ic4@f=pbi4yxe@zf@p_$4by5npv+w@3(41'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# ALLOWED_HOSTS = []
# ALLOWED_HOSTS = ['3.80.228.126']

# Application definition

BASE_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

LOCAL_APPS = [
    'apps.users',
    'apps.management',
    'apps.OCR',
    'apps.frontend',
]

THIRD_APPS = [
    'rest_framework',
    'django_filters',
    'rut_chile',
    'solo',
    'django_cron',
    "corsheaders",
    'django_rest_passwordreset',
]

CRON_CREDENCIAL= 'Nmi9IXfkKBUgyRk*pQ+1F9Xz@8OS7$1&E4^6eJTrdgKD$soC6'

INSTALLED_APPS = BASE_APPS + LOCAL_APPS + THIRD_APPS


REST_FRAMEWORK = { 
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'apps.users.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication'
    ),
    'DEFAULT_PERMISSION_CLASSES':(
        'rest_framework.permissions.IsAuthenticated',
    )
}

TOKEN_EXPIRED_AFTER = datetime.timedelta(hours=10)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    'apps.middleware.LogRestMiddleware',
]

CORS_ALLOW_ALL_ORIGINS: True

CORS_ALLOW_CREDENTIALS = True

ROOT_URLCONF = 'Transcriptor.urls'

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

WSGI_APPLICATION = 'Transcriptor.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'dfosmic3vq03p9',
        'USER': 'xvnkiwgepmxbmi',
        'PASSWORD':'0a8cfa127ba4dec9ccc58e39d6d990fa995cad63a47c2442130c3c1abe1e8f56',
        'HOST':'ec2-52-205-98-159.compute-1.amazonaws.com',
        'PORT':'5432'
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'America/Santiago'

USE_I18N = True

USE_L10N = True

USE_TZ = True   



AUTH_USER_MODEL = 'users.User'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#Segundos que dura un token (establecido en 10 horas)


#funcion para el proceso automatico 
CRON_CLASSES = [
    "apps.tasks.MyCronJob"
]


#ACA SE ESTABLECE EL CORREO QUE USARA EL SISTEMA PARA ENVIAR CORREOS, SE ESPECIFICÓ UNO DE EJEMPLOS PARA ENVIAR CORREOS DE TEST
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST_USER = "testrodaapi@gmail.com"
EMAIL_HOST ='smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_PASSWORD = 'tqhtssgnowedlown'



STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

LOGIN_URL = 'login'

STATIC_ROOT = '/var/www/Trans-site/assets/'
