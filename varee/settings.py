import os
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-temp-key'
DEBUG = True
ALLOWED_HOSTS = ['*']
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# ========================
# APPS
# ========================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'corsheaders',
    'store',
    'accounts',
  

    # ✅ backend apps (ONLY ONCE)
    'backend.users',
    'backend.products',
    'backend.cart',
    'backend.orders',
    'backend.contact',
    'backend.dashboard',
    'backend.wishlist',

]

# ========================
# MIDDLEWARE
# ========================
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOW_ALL_ORIGINS = True

# ========================
# URLS
# ========================
ROOT_URLCONF = 'varee.urls'

# ========================
# TEMPLATES
# ========================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        'DIRS': [BASE_DIR / 'backend' / 'templates'],

        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ========================
# DATABASE
# ========================


DATABASES = {
    'default': dj_database_url.parse(
       'postgresql://varee_db_user:YHU6so7f3KhSxxDZuCrduok1JkKsUz3s@dpg-d7ifjcnlk1mc739sf530-a.oregon-postgres.render.com/varee_db'
    )
}

EMAIL_HOST_USER = 'kavathiyapc1@gmail.com'
EMAIL_HOST_PASSWORD = 'wjpg ikfv splv yfxc'

# ========================
# STATIC FILES
# ========================
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / 'backend' / 'static'
]

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/home/'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ========================
# DRF
# ========================
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
}
CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:8000",
]
# ========================
# OTHER
# ========================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'