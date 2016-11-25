from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/', auth_views.login, {'template_name': 'login.html'}),
    url(r'^logout/', auth_views.logout, { 'template_name': 'logout.html' }),
    url(r'^order/', views.order, name='order'),
]
