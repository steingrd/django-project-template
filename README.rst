=======================
django-project-template
=======================

The project model created by the standard ``django-admin.py`` tool does
not promote best practices. 

The ``create_django_project.py`` script creates an alternate Django
project structure with functional skeleton applications and templates.
The main goal is to create a directory structure that promotes best
practices such as standalone applications and easily deployable units.

Project structure
=================

The project structure created by the script is a bit different than the
standard Django project structure::

myproject/
    environment.sh
    templates/
        base.html
        myapp/
            index.html
    scripts/
        manage.py
    python/
        myapp/
            __init__.py
            urls.py
    	    views.py
    	    forms.py
	    models.py
        myproject/
            __init__.py
    	    urls.py
    	    settings.py
    media/
        default.css









