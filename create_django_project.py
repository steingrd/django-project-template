#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2008 by Steingrim Dovland <steingrd@ifi.uio.no>

"""create-django-project.py

Creates a Django project directory structure with skeleton templates and
default views. The root directory is created in the current directory.

Usage:

    create-django-project.py [options] projectname 

-a NAME, --appname=NAME     name of default application, default is myapp

"""

import getopt
import os
import sys

ENVIRONMENT_SH_TEMPLATE = """#!/bin/bash -x

export DJANGO_SETTINGS_MODULE="{{ projectname }}.settings"
export PYTHONPATH="$PWD/python:$PYTHONPATH"
export PATH="$PWD/scripts:$PATH"
export DJANGO_TEMPLATE_PATH="$PWD/templates"
export DJANGO_MEDIA_ROOT="$PWD/media"
"""

DEFAULT_CSS_TEMPLATE = """/* default stylesheet, add styles here */
"""

MANAGE_PY_TEMPLATE = """#!/usr/bin/env python

if __name__ == "__main__":
    from django.core.management import execute_manager
    from os import getenv
    settings_module = getenv('DJANGO_SETTINGS_MODULE')
    settings = __import__(settings_module, locals(), globals(), [settings_module.split('.')[-1]])
    execute_manager(settings)
"""

BASE_HTML_TEMPLATE = """<html>
<head>
  {% block title %}
    <title>{{ projectname }}</title>
  {% endblock %}
    <link rel="stylesheet" href="/media/default.css" type="text/css" media="screen" />
  {% block extrahead %}
  {% endblock %}  
</head>
<body>
  {% block content %}
  {% endblock %}
</body>
</html>
"""

INDEX_HTML_TEMPLATE = """{% extends "base.html" %}
{% block content %}
Hello, world! Greetings from {{ appname }}
{% endblock %}
"""

PROJECT_URLS_PY_TEMPLATE = """from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('', 
  url(r'^admin/(.*)', admin.site.root),                     
  url(r'^$', 'django.views.generic.simple.redirect_to', { 'url': '/{{ appname }}/' }),
  url(r'^{{ appname }}/', include('{{ appname }}.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', 
        { 
            'document_root': settings.STATIC_ROOT
        }))

"""

APP_URLS_PY_TEMPLATE = """from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('', 
  url('^$', direct_to_template, {'template':'{{ appname }}/index.html'}),
)
"""

MODELS_PY_TEMPLATE = """
"""

VIEWS_PY_TEMPLATE = """
"""

FORMS_PY_TEMPLATE = """
"""

SETTINGS_PY_TEMPLATE = """import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
   ('Your Name', 'your.email@example.com'),
)

MANAGERS = ADMINS

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.sessions',

    '{{ appname }}',
)

STATIC_ROOT = 'media'

ROOT_URLCONF = '{{ projectname }}.urls'

TEMPLATE_DIRS = (
    os.getenv('DJANGO_TEMPLATE_PATH'),
)

TEMPLATE_CONTEXT_PROCESSORS =  (
    'django.core.context_processors.debug',
    'django.core.context_processors.auth',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
)

DATABASE_ENGINE = ''  
DATABASE_NAME = '' 
DATABASE_USER = ''
DATABASE_PASSWORD = ''
DATABASE_HOST = ''           
DATABASE_PORT = ''

TIME_ZONE = 'Europe/Oslo'
LANGUAGE = 'no'
LANGUAGE_CODE = 'no'
SITE_ID = 1
USE_I18N = True

MEDIA_ROOT = os.getenv('DJANGO_MEDIA_ROOT')
MEDIA_URL = 'http://localhost:8080/media/'
ADMIN_MEDIA_PREFIX = '/admin_media/'

SECRET_KEY = '{{ secretkey }}'
"""

def create_project_template(projectname, **options):
    if os.path.exists(projectname):
        print 'skipping %s, directory exists' % projectname
        return

    if 'appname' in options:
        appname = options['appname']
    else:
        appname = 'myapp'

    create_directory(projectname)
    create_directory(projectname, 'media')
    create_directory(projectname, 'python')
    create_directory(projectname, 'python', appname)
    create_directory(projectname, 'python', projectname)
    create_directory(projectname, 'scripts')
    create_directory(projectname, 'templates')
    create_directory(projectname, 'templates', appname)

    secretkey = generate_secret_key()
    context = { 'projectname' : projectname, 'appname' : appname, 'secretkey' : secretkey }

    render_template('', (projectname, 'python', appname, '__init__.py'), {})
    render_template(APP_URLS_PY_TEMPLATE, (projectname, 'python', appname, 'urls.py'), context)
    render_template(VIEWS_PY_TEMPLATE, (projectname, 'python', appname, 'views.py'), context)
    render_template(MODELS_PY_TEMPLATE, (projectname, 'python', appname, 'models.py'), context)
    render_template(FORMS_PY_TEMPLATE, (projectname, 'python', appname, 'forms.py'), context)

    render_template('', (projectname, 'python', projectname, '__init__.py'), {})
    render_template(PROJECT_URLS_PY_TEMPLATE, (projectname, 'python', projectname, 'urls.py'), context)
    render_template(SETTINGS_PY_TEMPLATE, (projectname, 'python', projectname, 'settings.py'), context)
    
    render_template(BASE_HTML_TEMPLATE, (projectname, 'templates', 'base.html'), context)
    render_template(INDEX_HTML_TEMPLATE, (projectname, 'templates', appname, 'index.html'), context)
    render_template(MANAGE_PY_TEMPLATE, (projectname, 'scripts', 'manage.py'), context)
    render_template(DEFAULT_CSS_TEMPLATE, (projectname, 'media', 'default.css'), context)
    render_template(ENVIRONMENT_SH_TEMPLATE, (projectname, 'environment.sh'), context)

def create_directory(dirname, *args):
    """
    Creates a directory named ``dirname`` if possible. Subdirectories of
    ``dirname`` can be specified in *args.

    Example: create_directory('foo', 'bar', 'zot') creates the
    directories foo/bar/zot/ in the current directory.
    
    """
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    
    if args:
        root = dirname
        for subdir in args:
            newdir = os.path.join(root, subdir)
            if not os.path.exists(newdir):
                os.mkdir(newdir)
            root  = newdir

def render_template(template_string, filepath, context):
    """
    Renders the template string ``template_string`` to the file path
    given as a list in ``filepath`` with ``context``.

    Example: render_template(string, ('foo', 'bar', 'zot.html'),
    context) renders the file zot.html in the directory foo/bar/.

    """
    for key, value in context.items():
        template_string = template_string.replace('{{ %s }}' % key, value)
    template_file = open(os.path.sep.join(filepath), 'w')
    template_file.write(template_string)
    template_file.close()

def generate_secret_key():
    """
    Generates a SECRET_KEY for Django settings module.
    """
    return ''.join([choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50)])

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ha:", ["help", "appname"])
    except getopt.error, msg:
        print msg
        print "for help use --help"
        sys.exit(2)

    options = {}

    for o, a in opts:
        if o in ("-h", "--help"):
            print __doc__
            sys.exit(0)
        if o in ("-a", "--appname"):
            options['appname' ] = a

    for a in args:
        create_project_template(a, **options)

if __name__ == "__main__":
    main()
