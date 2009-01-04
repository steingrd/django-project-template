#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2008, 2009 by Steingrim Dovland <steingrd@ifi.uio.no>

"""
Creates a runnable, functional Django project with two applications: a
project application and a default application. Applications are created
with sensible skeleton Python modules and templates.

Usage:

    create-django-project.py [options] projectname 

Options:

    -a NAME, --appname=NAME     name of application, default is myapp
    -q, --quiet                 supress informational output messages
    -h, --help                  show this message"""

import getopt
import os
import random
import stat
import sys


def create_project_template(projectname, **options):
    if os.path.exists(projectname):
        print 'skipping %s, directory exists' % projectname
        return

    if 'appname' in options:
        appname = options['appname']
    else:
        appname = 'myapp'

    if 'quiet' in options:
        quiet = options['quiet']
    else:
        quiet = False

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

    render_template('', {}, projectname, 'python', appname, '__init__.py')
    render_template(APP_URLS_PY_TEMPLATE, context, projectname, 'python', appname, 'urls.py')
    render_template(VIEWS_PY_TEMPLATE, context, projectname, 'python', appname, 'views.py')
    render_template(MODELS_PY_TEMPLATE, context, projectname, 'python', appname, 'models.py')
    render_template(FORMS_PY_TEMPLATE, context, projectname, 'python', appname, 'forms.py')
    render_template('', context, projectname, 'python', projectname, '__init__.py')
    render_template(PROJECT_URLS_PY_TEMPLATE, context, projectname, 'python', projectname, 'urls.py')
    render_template(SETTINGS_PY_TEMPLATE, context, projectname, 'python', projectname, 'settings.py')
    render_template(SETTINGS_PROD_PY_TEMPLATE, context, projectname, 'python', projectname, 'settings_prod.py')
    render_template(BASE_HTML_TEMPLATE, context, projectname, 'templates', 'base.html')
    render_template(TEMPLATE_404_TEMPLATE, {}, projectname, 'templates', '404.html')
    render_template(TEMPLATE_500_TEMPLATE, {}, projectname, 'templates', '500.html')
    render_template(INDEX_HTML_TEMPLATE, context, projectname, 'templates', appname, 'index.html')
    render_template(DEFAULT_CSS_TEMPLATE, context, projectname, 'media', 'default.css')
    render_template(MANAGE_PY_TEMPLATE, context, projectname, 'manage.py')
    render_template(ENVIRONMENT_SH_TEMPLATE, context, projectname, 'environment.sh')
    render_template(GENERATE_FCGI_SH_TEMPLATE, context, projectname, 'scripts', 'generate_fcgi.sh')

    # set executable flag for manage.py
    os.chmod(os.path.join(projectname, 'manage.py'), stat.S_IRWXU | stat.S_IRGRP | stat.S_IROTH)

    if not quiet:
        print 'Project %s created with application %s' % (projectname, appname)

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


def render_template(template_string, context, *filepath):
    """
    Renders the template string ``template_string`` to the file path
    given as a list in ``filepath`` with ``context``.

    Example: render_template(string, ('foo', 'bar', 'zot.html'),
    context) renders the file zot.html in the directory foo/bar/.

    """
    for key, value in context.items():
        template_string = template_string.replace('{{ %s }}' % key, value)
    template_file = open(os.path.join(*filepath), 'w')
    template_file.write(template_string)
    template_file.close()


def generate_secret_key():
    """
    Generates a SECRET_KEY for Django settings module.
    """
    return ''.join([random.choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') 
                    for i in range(50)])


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ha:q", ["help", "appname=", "quiet"])
    except getopt.error, msg:
        print msg
        print "for help use --help"
        sys.exit(2)

    options = {}

    if not args:
        print __doc__
        sys.exit(0)

    for o, a in opts:
        if o in ("-h", "--help"):
            print __doc__
            sys.exit(0)
        if o in ("-a", "--appname"):
            options['appname' ] = a
        if o in ("-q", "--quiet"):
            options['quiet' ] = True

    for a in args:
        create_project_template(a, **options)


ENVIRONMENT_SH_TEMPLATE = """#!/bin/bash -x

export PYTHONPATH="$PWD/python:$PYTHONPATH"
export PATH="$PWD/scripts:$PATH"
export DJANGO_SETTINGS_MODULE="{{ projectname }}.settings"
export DJANGO_TEMPLATE_PATH="$PWD/templates"
export DJANGO_MEDIA_ROOT="$PWD/media"
"""

DEFAULT_CSS_TEMPLATE = """/* default stylesheet, add styles here */
"""

MANAGE_PY_TEMPLATE = """#!/usr/bin/env python

from django.core.management import execute_manager
from os import getcwd, environ, path
import sys

if __name__ == "__main__":
    environ['DJANGO_SETTINGS_MODULE'] = '{{ projectname }}.settings'
    environ['DJANGO_MEDIA_ROOT'] = path.join(getcwd(), 'media')
    environ['DJANGO_TEMPLATE_PATH'] = path.join(getcwd(), 'templates')
    sys.path.insert(0, path.join(getcwd(), 'python'))
    settings_module = '{{ projectname }}.settings'
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

TEMPLATE_404_TEMPLATE = """{% extends "base.html" %}
{% block content %}
<h1>404 Not Found</h1>
<p>Resource {{ request_path }} not found</p>
{% endblock %}
"""

TEMPLATE_500_TEMPLATE = """{% extends "base.html" %}
{% block content %}
<h1>500 Internal Server Error</h1>
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
from django.db import models
 
class Entry(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'entries'
 
    def __unicode__(self):
        return self.title
"""

VIEWS_PY_TEMPLATE = """
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse

def {{ appname }}_index(request):
    return HttpResponse('Hello, {{ appname }}')
"""

FORMS_PY_TEMPLATE = """
"""

SETTINGS_PROD_PY_TEMPLATE = """from settings import *

DATABASE_ENGINE = ''
DATABASE_NAME = ''
DATABASE_USER = ''
DATABASE_PASSWORD = ''
DATABASE_HOST = ''
DATABASE_PORT = ''

DEBUG = False
TEMPLATE_DEBUG = False
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

DATABASE_ENGINE = 'sqlite3'  
DATABASE_NAME = '{{ projectname }}.db' 
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

GENERATE_FCGI_SH_TEMPLATE = """#!/bin/bash
for dir in templates python media; do
    if [ ! -d "$dir" ]; then
	echo "expected directory '$dir' in current directory";
	echo "are you running $(basename $0) from project root?";
	exit 1;
    fi
done
cat <<EOF
#!/usr/bin/env python
import sys, os

sys.path.insert(0, "$PWD/python")

from django.core.handlers.wsgi import WSGIHandler
from flup.server.fcgi import WSGIServer

os.chdir("$PWD")

os.environ['DJANGO_MEDIA_ROOT'] = '$PWD/media'
os.environ['DJANGO_TEMPLATE_PATH'] = '$PWD/templates'
os.environ['DJANGO_SETTINGS_MODULE'] = '{{ projectname }}.settings_prod'

WSGIServer(WSGIHandler()).run()
EOF
"""


if __name__ == "__main__":
    main()
