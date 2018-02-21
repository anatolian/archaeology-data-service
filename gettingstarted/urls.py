# URL router for Django app
# Author: Christopher Besser
from django.conf.urls import include, url
from django.urls import path
import hello.views
urlpatterns = [
    url(r'^$', hello.views.index, name = 'index'),
    url(r'^test_connection', hello.views.test_connection, name = 'Test Connections'),
    url(r'^get_area_eastings', hello.views.get_area_eastings, name = 'Fetch Eastings'),
    url(r'^get_area_northings', hello.views.get_area_northings, name = 'Fetch Northings'),
    url(r'^get_context_numbers', hello.views.get_context_numbers, name = 'Fetch Contexts'),
    url(r'^get_sample_numbers', hello.views.get_sample_numbers, name = 'Fetch Samples'),
    url(r'^get_sample', hello.views.get_sample, name = 'Fetch Sample'),
    url(r'^set_weight', hello.views.set_weight, name = 'Set Weight'),
    url(r'^add_property', hello.views.add_property, name = 'Add Meta-variable'),
    url(r'^get_property', hello.views.get_property, name = 'Get Meta-variable'),
    url(r'^upload_file', hello.views.upload_file, name = 'Upload to S3'),
    url(r'^get_image_urls', hello.views.get_image_urls, name = 'Get S3 URLs')
]