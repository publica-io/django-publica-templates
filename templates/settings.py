from django.conf import settings


FILEFIELD_PATH = getattr(
    settings, 'TEMPLATES_FILEFIELD_PATH', 'templates/'
)
