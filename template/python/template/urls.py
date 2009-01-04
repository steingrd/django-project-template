#!/usr/bin/env python

from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',
  url(r'^admin/(.*)', admin.site.root),
  url(r'^$', 'django.views.generic.simple.redirect_to',
      {'url': '/myapp/'}),
  url(r'^myapp/', include('myapp.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_ROOT}))
