import os
import sys

from django.core.wsgi import get_wsgi_application

sys.path.append(r'F:/django_wzb/wzb')
os.environ['DJANGO_SETTINGS_MODULE'] = 'wzb.settings'
application = get_wsgi_application()

