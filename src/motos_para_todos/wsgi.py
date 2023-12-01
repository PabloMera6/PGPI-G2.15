"""
WSGI config for motos_para_todos project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise
from django.conf import settings
BASE_DIR = settings.BASE_DIR

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "motos_para_todos.settings")

application = get_wsgi_application()

application = WhiteNoise(application, root=os.path.join(BASE_DIR, 'staticfiles'))

