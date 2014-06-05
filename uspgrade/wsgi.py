"""
WSGI config for uspgrade project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os, sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "uspgrade.settings")

PATH = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))
sys.path.append(PATH)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

