from django.conf.urls import url
from . import views


urlpatterns = [

    url(r'^download/$', views.download, name='download'),

    # url(r'^insert/$', views.insert, name='insert'),
    # url(r'^edit/(\d+)$', views.edit, name='edit'),
    url(r'^printPayment/(\d+)$', views.printPayment, name='printPayment'),

    # url(r'^insertHandle/$', views.insertHandle, name='insertHandle'),
]
