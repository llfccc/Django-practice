# coding=utf-8
"""wzb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
# from stockCode import views as stockCode_views
from . import views as index_views
from django.contrib.auth import urls as auth_urls
# from django.contrib.auth import views as auth_views
import notifications.urls


urlpatterns = [
    url(r'^$', index_views.index),
    url(r'^hello/$', index_views.hello),
    url(r'^admin/', admin.site.urls),
    url(r'^test/$', index_views.test),
    url(r'^fetchNotification/$', index_views.fetchNotification),
    url(r'^stockCode/', include('stockCode.urls')),
    url(r'^payment/', include('payment.urls')),
    url(r'^keyEvent/', include('keyEvent.urls')),
    url(r'^supplierList/', include('supplierList.urls',namespace="supplierList")),
    url(r'^accounts/', include('accounts.urls')),
    url('^inbox/notifications/', include(notifications.urls, namespace='notifications')),
]
