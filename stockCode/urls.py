from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^upload_file/$', views.upload_file, name='upload_file'),
    url(r'^insertApplicant/$', views.insertApplicant, name='insertApplicant'),
    url(r'^showUnCode/$', views.showUnCode, name='showUnCode'),
    url(r'^showAlreadyCode/$', views.showAlreadyCode, name='showAlreadyCode'),
    url(r'^editCode/$', views.editCode, name='editCode'),

    url(r'^downloadZip/$', views.downloadZip, name='downloadZip'),
    url(r'^downloadModel/$', views.downloadModel, name='downloadModel'),


    url(r'^varifyCode/$', views.varifyCode, name='varifyCode'),
    url(r'^receiveCode/$', views.receiveCode, name='receiveCode'),
    url(r'^showAllAddCode/$', views.showAllAddCode, name='showAllAddCode'),
    url(r'^varifyApplication/$', views.varifyApplication, name='varifyApplication'),
    url(r'^dataStatistics/$', views.dataStatistics, name='dataStatistics'),
    url(r'^delCode/(\d+)/$', views.delCode, name='delCode'),


]
