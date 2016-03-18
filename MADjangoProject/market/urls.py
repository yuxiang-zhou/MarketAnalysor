from django.conf.urls import url
from django.contrib.auth.decorators import login_required, permission_required

from . import views

app_name = 'market'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^list/$', views.ListView.as_view(), name='list'),
    url(r'^list/(?P<catagory>[0-9a-zA-Z]+)$', views.ListView.as_view(), name='clist'),
    url(r'^detail/(?P<symbol>...+)$', views.DetailView.as_view(), name='detail'),
    url(r'^account/$', login_required(views.AccountView.as_view()), name='account'),
    url(r'^fav/$', login_required(views.SelectionView.as_view()), name='account'),
    url(r'^news/$', views.NewsView.as_view(), name='news'),
    url(r'^sectors/$', views.SectorView.as_view(), name='sectors'),
    # APIs
    url(r'^api/history/sector/(?P<sector>.+)$', views.historysector, name='historysector'),
    url(r'^api/history/stock/(?P<symbol>...+)$', views.history, name='history'),
    url(r'^api/list/(?P<indices>.*)$', views.list, name='api.list'),
    url(r'^api/detail/(?P<symbol>.+)$', views.detail, name='api.detail'),
]
