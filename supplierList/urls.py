from django.conf.urls import url
from . import views


# app_name='supplierList'
urlpatterns = [
    url(r'^querySupplier/$', views.querySupplier, name='querySupplier'),
    url(r'^addNewSupplier/$', views.addNewSupplier, name='addNewSupplier'),
    url(r'^info/([0-9]+)/$', views.info, name='info'),
    url(r'^updateAll/$', views.updateAll, name='updateAll'),
    url(r'^showDocument/$', views.showDocument, name='showDocument'),

    url(r'^queryOptionalSupplier/$', views.queryOptionalSupplier, name='queryOptionalSupplier'),
    url(r'^addNewOptionalSupplier/$', views.addNewOptionalSupplier, name='addNewOptionalSupplier'),
    url(r'^infoOptional/([0-9]+)/$', views.infoOptional, name='infoOptional'),
    url(r'^updateAllOptional/$', views.updateAllOptional, name='updateAllOptional'),
    url(r'^dataStatistics/$', views.dataStatistics, name='dataStatistics'),
]
