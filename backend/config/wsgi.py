"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os
import sys
from django.core.management import call_command

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Auto-migrate and seed on startup (for Render free tier)
try:
    call_command('migrate', '--noinput')
    call_command('seed_demo')
except Exception as e:
    pass

application = get_wsgi_application()
