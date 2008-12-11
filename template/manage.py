#!/usr/bin/env python

from django.core.management import execute_manager
from os import getcwd, environ, path
import sys

if __name__ == "__main__":
    environ['DJANGO_SETTINGS_MODULE'] = 'template.settings'
    environ['DJANGO_MEDIA_ROOT'] = path.join(getcwd(), 'media')
    environ['DJANGO_TEMPLATE_PATH'] = path.join(getcwd(), 'templates')
    sys.path.insert(0, path.join(getcwd(), 'python'))
    settings_module = 'template.settings'
    settings = __import__(settings_module, locals(), globals(), [settings_module.split('.')[-1]])
    execute_manager(settings)
