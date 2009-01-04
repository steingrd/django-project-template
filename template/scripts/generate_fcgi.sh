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

os.chdir("$PWD")

os.environ['DJANGO_MEDIA_ROOT'] = '$PWD/media'
os.environ['DJANGO_TEMPLATE_PATH'] = '$PWD/templates'
os.environ['DJANGO_SETTINGS_MODULE'] = 'template.settings_prod'

from django.core.servers.fastcgi import runfastcgi
runfastcgi(method="threaded", daemonize="false")
EOF
