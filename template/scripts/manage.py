#!/usr/bin/env python

if __name__ == "__main__":
    from django.core.management import execute_manager
    from os import getenv
    settings_module = getenv('DJANGO_SETTINGS_MODULE')
    settings = __import__(settings_module, locals(), globals(), [settings_module.split('.')[-1]])
    execute_manager(settings)
