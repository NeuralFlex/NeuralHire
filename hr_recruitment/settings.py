import os
from pathlib import Path
import dj_database_url
import os
from dotenv import load_dotenv
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
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

# Database Configuration
# Use SQLite for local development if DB environment variables are not set
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')

if DB_NAME and DB_USER and DB_PASSWORD and DB_HOST:
    # Use PostgreSQL if all DB env vars are provided
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': DB_NAME,
            'USER': DB_USER,
            'PASSWORD': DB_PASSWORD,
            'HOST': DB_HOST,
            'PORT': os.getenv('DB_PORT', '5432'),
        }
    }
else:
    # Default to SQLite for local development
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
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
    'PAGE_SIZE': 10,
}


# --- STATIC & MEDIA FILES ---
# --- AWS S3 CONFIGURATION ---
AWS_REGION = os.environ.get('AWS_REGION', '')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME', '')

# Use S3 if AWS credentials are provided, otherwise use local storage
USE_S3 = bool(AWS_REGION and AWS_STORAGE_BUCKET_NAME)

if USE_S3:
    # AWS S3 Configuration
    AWS_S3_REGION_NAME = AWS_REGION
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com'
    AWS_QUERYSTRING_AUTH = False
    
    DEFAULT_FILE_STORAGE = 'hr_recruitment.storage_backends.PrivateMediaStorage'
    STATICFILES_STORAGE = 'hr_recruitment.storage_backends.StaticRootStorage'
    
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/resumes/'
else:
    # Local file storage for development
    STATIC_URL = '/static/'
    MEDIA_URL = '/media/'
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

# Standard settings still needed by collectstatic
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_ROOT = BASE_DIR / "media"