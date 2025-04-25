import os
from pathlib import Path
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Secret key for Django
SECRET_KEY = 'django-insecure-5s2zep#tjs!+(t^3wv9!flzg_ffb+eag)gniediw%p8d7hu0)k'

# Debugging and allowed hosts
DEBUG = True
ALLOWED_HOSTS = ['*']

# Site configuration
SITE_ID = 1

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'qrcode',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "allauth.account.middleware.AccountMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

ROOT_URLCONF = 'setup.urls'

# Templates configuration
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = 'setup.wsgi.application'

# Database configuration (using SQLite here, but adjust as needed)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.oracle',
#         'NAME': f"(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST={os.getenv('DB_HOST')})(PORT={os.getenv('DB_PORT')}))(CONNECT_DATA=(SERVER=DEDICATED)(SERVICE_NAME={os.getenv('DB_SERVICE_NAME')})))",
#         'USER': os.getenv('DB_USER'),
#         'PASSWORD': os.getenv('DB_PASSWORD'),
#     }
# }


DATABASES = {
    'default': dj_database_url.config(
        default='postgresql://festao_rqog_user:F37fZnKHpBbTAcOPZrWCNHilaMuv591Z@dpg-d05qjbpr0fns73ekbef0-a.oregon-postgres.render.com/festao_rqog',
        conn_max_age=600,
        ssl_require=True  # Certifica que a conexão usa SSL
    )
}


# Password validation
AUTH_PASSWORD_VALIDATORS = []

# Localization settings
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, images)
STATIC_URL = 'static/'

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'setup/static')]

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Authentication settings
# O login será feito apenas com o username
ACCOUNT_AUTHENTICATION_METHOD = "username"
ACCOUNT_EMAIL_REQUIRED = False  # E-mail não será obrigatório
ACCOUNT_USERNAME_REQUIRED = True  # Username será obrigatório
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = True
ACCOUNT_EMAIL_VERIFICATION = "optional"  # Desabilita verificação do e-mail
ACCOUNT_SESSION_REMEMBER = True  # Mantém o login ativo após autenticação
ACCOUNT_UNIQUE_EMAIL = False  # Permite múltiplos usuários com o mesmo e-mail
ACCOUNT_FORMS = {
    'signup': 'accounts.forms.CustomSignupForm',
}

LOGIN_URL = '/login/'  # URL para página de login personalizada
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Social account settings
SOCIALACCOUNT_LOGIN_ON_GET = True
ACCOUNT_LOGOUT_ON_GET = True

# Email backend configuration (for development purposes)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
