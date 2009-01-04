#!/usr/bin/env python

from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template


urlpatterns = patterns('',
  url('^$', direct_to_template, {'template': 'myapp/index.html'}),
)
