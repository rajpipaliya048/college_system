from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-(advk8gos=zsx24gjac=dww%rmb4_-8=#z+ww4gle49m6tkf@#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['www.mycollege.com','course.mycollege.com', 'mycollege.com','1200-117-219-102-26.ngrok-free.app']

CSRF_TRUSTED_ORIGINS = [
    'https://1200-117-219-102-26.ngrok-free.app'
]

# EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
# EMAIL_USE_TLS = True  
# EMAIL_HOST = 'smtp.gmail.com'  
# EMAIL_HOST_USER = 'rajpatelfordjango@gmail.com'  
# EMAIL_HOST_PASSWORD = 'R@j123456'  
# EMAIL_PORT = 587  

EMAIL_HOST = '127.0.0.1'
EMAIL_PORT = 1025
EMAIL_USE_TLS = False
    
LOGIN_URL = '/login/' 

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'widget_tweaks',
    'users',
    'course',
    'paypal.standard.ipn',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'users.middleware.RequestLoggingMiddleware',
    'users.middleware.AdminAccessOnlyMiddleware',
    'users.middleware.AddSkillsMiddleware',

]

ROOT_URLCONF = 'college.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'college.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

PAYPAL_RECEIVER_EMAIL = 'sb-n1470927897205@business.example.com'
PAYPAL_TEST = True

CASHFREE_CLIENT_ID = "TEST1004636252a7a957fe37897b3e1426364001"
CASHFREE_CLIENT_SECRET = "TESTda62d9e12f45596682807043257c2cab9ea9c1bd"

STRIPE_PUBLISHABLE_KEY = 'pk_test_51O6YLUSBeOYLWagPZMg7d5G2hsazpZNUR1hLv7RB0Gz4MxLm7eqxG9ORK2CD6XC9NK9Il2GdOKMkY4PWkqW8vyTO00DtxsPBjj'
STRIPE_SECRET_KEY = 'sk_test_51O6YLUSBeOYLWagPuwpvcM1ArdAVcyrTyGwokvIRuSDhlAfyUnjtbjnj5T2258PeqzXq3KBScyS6GfbdhDJekj5X00CI2pMtwS'


RAZORPAY_KEY_ID = 'rzp_test_cbbT64IJEOxbfw'
RAZORPAY_KEY_SECRET = 'DewJLZJWfFLLnBJx4o0hv2Vr'

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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'assets'),
)


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin-allow-popups"


CELERY_BROKER_URL = "redis://localhost:6379"
CELERY_RESULT_BACKEND = "redis://localhost:6379"
CELERY_TASK_TRACK_STARTED = True
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        },
        "KEY_PREFIX": "example"
    }
}