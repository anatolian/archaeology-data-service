from django.conf.urls import include, url
from django.urls import path
import hello.views
urlpatterns = [
    url(r'^$', hello.views.index, name = 'index'),
    url(r'^test', hello.views.test, name = 'test'),
    url(r'^relations', hello.views.relations, name = 'relations'),
    url(r'^get_area_eastings', hello.views.get_area_eastings, name = 'get_area_eastings'),
    url(r'^get_area_northings/<int:easting>', hello.views.get_area_northings, name = 'get_area_northings')
]