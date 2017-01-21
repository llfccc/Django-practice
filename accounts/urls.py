from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^login/$', views.login, name='accounts'),
    url(r'^logout/$', views.logout, name='accounts'),
    url(r'^register/$', views.register, name='accounts'),
    url(r'^changepwd/$', views.changepwd, name='accounts'),

]
