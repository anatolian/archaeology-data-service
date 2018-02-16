# URL router for Django app
# Author: Christopher Besser
from django.conf.urls import include, url
from django.urls import path
import hello.views
urlpatterns = [
    url(r'^$', hello.views.index, name = 'index'),
    url(r'^relations', hello.views.relations, name = 'relations'),
    url(r'^get_area_eastings', hello.views.get_area_eastings, name = 'get_area_eastings'),
    url(r'^get_area_northings', hello.views.get_area_northings, name = 'get_area_northings'),
    url(r'^get_context_numbers', hello.views.get_context_numbers, name = 'get_context_numbers'),
    url(r'^get_sample_numbers', hello.views.get_sample_numbers, name = 'get_sample_numbers'),
    url(r'^get_sample', hello.views.get_sample, name = 'get_sample'),
    url(r'^set_weight', hello.views.set_weight, name = 'set_weight'),
    url(r'^add_property', hello.views.add_property, name = 'add_property'),
    url(r'^get_property', hello.views.get_property, name = 'get_property'),
    url(r'^add_image', hello.views.add_image, name = 'add_image'),
    url(r'^upload_file', hello.views.upload_file, name = 'upload_file')
]