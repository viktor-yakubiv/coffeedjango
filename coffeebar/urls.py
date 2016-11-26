from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

from . import views

urlpatterns_order = [
    url(r'^$', views.index, name='order'),
    url(r'^add/', views.add_item, name='order_add'),
    url(r'^checkout/', views.checkout, name='order_checkout'),
    url(r'^list/$', views.list_orders, name='order_list'),
]

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'order/', include(urlpatterns_order)),
    url(r'^login/', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/', auth_views.logout, {'template_name': 'logout.html'}, name='logout'),
]
