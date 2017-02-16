from django.conf.urls import url
from . import views


urlpatterns = [

    url(r'^showAllPayment/$', views.showAllPayment, name='showAllPayment'),

    url(r'^upload_file/$', views.upload_file, name='upload_file'),
    url(r'^edit/(\d+)$', views.edit, name='edit'),
    url(r'^delete/(\d+)$', views.delete, name='delete'),
    url(r'^editHandle/$', views.editHandle, name='editHandle'),
    url(r'^insertPayment/$', views.insertPayment, name='insertPayment'),

    url(r'^download/$', views.download, name='download'),
]
