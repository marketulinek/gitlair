from pathlib import Path

ROOT_URLCONF = 'gitlair'
DEBUG = True
SECRET_KEY = 'my-secret-key'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [Path(__file__).parent / 'templates'],
    }
]
