import os
import sys

path = '/var/lib/djangoapp'
if path not in sys.path:
	sys.path.append(path)

path = '/var/lib/djangoapp/mysite'
if path not in sys.path:
	sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()



