import os
from pathlib import Path
import dj_database_url
import os
from dotenv import load_dotenv
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# --- CORE CONFIGURATION ---

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'dev-secret-key-change-me')

DEBUG = os.environ.get('DJANGO_DEBUG', '0') == '1'

# Define known production host for explicit safety
RAILWAY_HOST = 'web-production-9687.up.railway.app' 
NETLIFY_HOST = 'https://neuralhirefrontend.netlify.app'

if DEBUG:
    ALLOWED_HOSTS = ['*']
else:
    env_hosts = os.environ.get('DJANGO_ALLOWED_HOSTS')
    if env_hosts:
        ALLOWED_HOSTS = env_hosts.split(',')
    else:
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
CORS_ALLOW_HEADERS = [
    "authorization",
    "content-type",
    "accept",
    "origin",
    "user-agent",
    "x-requested-with",
]

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

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
    'storages',
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

# DATABASES = {
#     'default': dj_database_url.config(
#         conn_max_age=600,
#         default='sqlite:///db.sqlite3' 
#     )
# }
# Railway
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }local 
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', ''),
        'USER': os.getenv('DB_USER', ''),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', ''),
        'PORT': os.getenv('DB_PORT', ''),
    }
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
    'PAGE_SIZE': 20,
}


# --- STATIC & MEDIA FILES ---
# --- AWS S3 CONFIGURATION ---
AWS_REGION = os.environ.get('AWS_REGION') 
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = AWS_REGION
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com'


AWS_QUERYSTRING_AUTH = False 



DEFAULT_FILE_STORAGE = 'hr_recruitment.storage_backends.PrivateMediaStorage'


STATICFILES_STORAGE = 'hr_recruitment.storage_backends.StaticRootStorage'

# URLs for static and media files now point to S3
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/resumes/'

# Standard settings still needed by collectstatic
STATIC_ROOT = BASE_DIR / "staticfiles"