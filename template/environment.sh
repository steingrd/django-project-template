#!/bin/bash -x

export PYTHONPATH="$PWD/python:$PYTHONPATH"
export PATH="$PWD/scripts:$PATH"
export DJANGO_SETTINGS_MODULE="template.settings"
export DJANGO_TEMPLATE_PATH="$PWD/templates"
export DJANGO_MEDIA_ROOT="$PWD/media"
