from django.conf.urls import url
from . import views


urlpatterns = [

    url(r'^showAllPayment/$', views.showAllPayment, name='showAllPayment'),

    # url(r'^insert/$', views.insert, name='insert'),
    # url(r'^edit/(\d+)$', views.edit, name='edit'),
    url(r'^printPayment/(\d+)$', views.printPayment, name='printPayment'),

    # url(r'^insertHandle/$', views.insertHandle, name='insertHandle'),
]
