gitstats.ep.io
==============

Dulwich & highcharts.com powered statistics about git repositories.


Run locally
-----------

1. ``git clone git://github.com/ojii/gitstats.ep.io.git``
2. ``cd gitstats.ep.io``
3. ``virtualenv env --no-site-packages``
4. ``source env/bin/activate``
5. ``pip install -Ur requirements.txt``
6. Create a file ``src/local_settings.py`` with your database settings, enable
   debug mode (if you want) and disable the django-secure settings.
7. ``python src/manage.py syncdb``
8. ``python src/manage.py migrate``
9. ``python src/manage.py runserver``
