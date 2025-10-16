import os
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# --- CORE CONFIGURATION ---

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'dev-secret-key-change-me')

# 1. FIXED DEBUG DEFAULT: Defaults to '0' (False) if DJANGO_DEBUG is not set, 
# which is safer for production environments.
DEBUG = os.environ.get('DJANGO_DEBUG', '0') == '1'

# Define known production host for explicit safety
RAILWAY_HOST = 'web-production-9687.up.railway.app' 
NETLIFY_HOST = 'https://neuralhirefrontend.netlify.app'

# 2. FIXED ALLOWED_HOSTS LOGIC: Handles production hosts robustly.
if DEBUG:
    # Allow all hosts for local development
    ALLOWED_HOSTS = ['*']
else:
    # Priority 1: Use environment variable if it exists
    env_hosts = os.environ.get('DJANGO_ALLOWED_HOSTS')
    if env_hosts:
        ALLOWED_HOSTS = env_hosts.split(',')
    else:
        # Priority 2: Hardcode essential production hosts for guaranteed functionality
        ALLOWED_HOSTS = [
            RAILWAY_HOST, 
            # Note: Allowed Hosts usually only need the API domain, 
            # but sometimes include the frontend if it's hitting non-API views.
            '.railway.app', # Safe wildcard for Railway subdomains
        ]

# --- CORS & SECURITY ---

# Set this to False to be strict in production, but leaving it True for now based on your provided code
CORS_ALLOW_ALL_ORIGINS = True 

# If CORS_ALLOW_ALL_ORIGINS = False, this list is used:
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://neuralhirefrontend.netlify.app", 
]
# Note: Since CORS_ALLOW_ALL_ORIGINS is True, this list is currently ignored.

X_FRAME_OPTIONS = 'ALLOWALL'
ROOT_URLCONF = 'hr_recruitment.urls'

# --- INSTALLED APPS & MIDDLEWARE ---

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'corsheaders',

    'recruitment',
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
    'whitenoise.middleware.WhiteNoiseMiddleware',
]


# --- TEMPLATES, WSGI, DATABASE ---

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

WSGI_APPLICATION = 'hr_recruitment.wsgi.application'

DATABASES = {
    'default': dj_database_url.config(
        conn_max_age=600,
        # Ensure you set the DATABASE_URL environment variable on Railway
        default='sqlite:///db.sqlite3' 
    )
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- DJANGO REST FRAMEWORK (DRF) ---

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated', # Protect endpoints by default
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication', 
        'rest_framework.authentication.SessionAuthentication', 
        'rest_framework.authentication.BasicAuthentication', 
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}


# --- STATIC & MEDIA FILES ---

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'