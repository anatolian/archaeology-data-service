# URL router for Django app
# Author: Christopher Besser
from django.conf.urls import include, url
from django.urls import path
import hello.views
urlpatterns = [
    url(r'^$', hello.views.index, name = 'index'),
    url(r'^test_connection', hello.views.test_connection, name = 'Test Connections'),
    url(r'^get_eastings', hello.views.get_eastings, name = 'Fetch Eastings'),
    url(r'^get_northings', hello.views.get_northings, name = 'Fetch Northings'),
    url(r'^get_finds', hello.views.get_finds, name = 'Fetch Finds'),
    url(r'^get_find_colors', hello.views.get_find_colors, name = 'Fetch Find Colors'),
    url(r'^get_find', hello.views.get_find, name = 'Fetch Find'),
    url(r'^set_weight', hello.views.set_weight, name = 'Set Weight'),
    url(r'^add_property', hello.views.add_property, name = 'Add Meta-variable'),
    url(r'^get_property', hello.views.get_property, name = 'Get Meta-variable'),
    url(r'^upload_file', hello.views.upload_file, name = 'Upload to S3'),
    url(r'^get_image_urls', hello.views.get_image_urls, name = 'Get S3 URLs'),
    url(r'^get_next_find_id', hello.views.get_next_find_id, name = 'Get next find ID'),
    url(r'^get_previous_find_id', hello.views.get_previous_find_id, name = 'Get previous find ID'),
    url(r'^set_color', hello.views.set_color, name = 'Set find color')
    url(r'^insert_find', hello.views.insert_find, name = 'Insert a new find')
]