from django.conf.urls import url
from . import views


urlpatterns = [

    url(r'^showAllKeyEvents/$', views.showAllKeyEvents, name='showAllKeyEvents'),

    url(r'^insert/$', views.insert, name='insert'),
    url(r'^edit/(\d+)$', views.edit, name='edit'),
    url(r'^printKey/(\d+)$', views.printKey, name='printKey'),

    url(r'^insertHandle/$', views.insertHandle, name='insertHandle'),
]
