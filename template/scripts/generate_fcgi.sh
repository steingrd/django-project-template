#!/bin/bash
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
os.environ['DJANGO_SETTINGS_MODULE'] = 'template.settings'

WSGIServer(WSGIHandler()).run()
EOF
