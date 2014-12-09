import os
import sys

path = '/home/burt/dj-proj'
if path not in sys.path:
	sys.path.append(path)

path = '/home/burt/dj-proj/mysite'
if path not in sys.path:
	sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()



