from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

from . import views

app_name = 'coffeebar'

urlpatterns_order = [
    url(r'^$', views.order_view, name='order'),
    url(r'^add/', views.order_add_item, name='order_add'),
    url(r'^remove/', views.order_remove_item, name='order_remove'),
    url(r'^checkout/', views.order_checkout, name='order_checkout'),
    url(r'^list/$', views.order_list, name='order_list'),
    # url(r'^details/(?P<order_id>[0-9]+/)', views.order_details, name='order_details')
]

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'order/', include(urlpatterns_order)),

    # django auth
    url(r'^login/', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/', auth_views.logout, {'template_name': 'logout.html'}, name='logout'),
]
