from django.conf.urls import url

from . import views

app_name = 'market'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^list/$', views.ListView.as_view(), name='list'),
    url(r'^list/(?P<catagory>[0-9a-zA-Z]+)$', views.ListView.as_view(), name='list'),
    url(r'^detail/(?P<symbol>[0-9a-zA-Z]+)$', views.DetailView.as_view(), name='detail'),
    url(r'^history/(?P<symbol>[0-9a-zA-Z]+)$', views.history, name='history'),
]
