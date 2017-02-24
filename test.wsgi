import os, sys
wsgi_dir = os.path.abspath(os.path.dirname(__file__))
project_dir = os.path.dirname(wsgi_dir)
sys.path.append(project_dir)
sys.path.append(r'F:/django_wzb/wzb')

project_settings = os.path.join(project_dir,'settings')
os.environ['DJANGO_SETTINGS_MODULE'] ='wzb.settings'
import django.core.handlers.wsgi
application =django.core.handlers.wsgi.WSGIHandler()