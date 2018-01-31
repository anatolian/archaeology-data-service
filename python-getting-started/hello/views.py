from django.shortcuts import render
from django.http import HttpResponse
import psycopg2
import os
# Store the values for your own database in environment variables prior to running!
hostname = os.environ.get('postgres-hostname')
username = os.environ.get('postgres-username')
password = os.environ.get('postgres-password')
database = os.environ.get('postgres-database')
# from .models import Greeting
# Main page
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, 'index.html')

# def db(request):
#     greeting = Greeting()
#     greeting.save()
#     greetings = Greeting.objects.all()
#     return render(request, 'db.html', {'greetings': greetings})

def test(request):
	connection = psycopg2.connect(host = hostname, user = username, password = password, dbname = database)
	cursor = connection.cursor()
	cursor.execute("SELECT * FROM Areas;")
	response = 'area_easting | area_northing | area_key | status';
	for easting, northing, key, status in cursor.fetchall():
		response = response + "\n" + str(easting) + " | " + str(northing) + " | " + key + " | " + status
	connection.close()
	return HttpResponse(response, content_type = 'text/plain')

# Get the relation names in the database
def relations(request):
	connection = psycopg2.connect(host = hostname, user = username, password = password, dbname = database)
	cursor = connection.cursor()
	cursor.execute("SELECT relname FROM pg_stat_user_tables WHERE schemaname = 'public';")
	response = 'relname'
	count = 0;
	for relname in cursor.fetchall():
		count += 1
		# Python seems to think this is a tuple for some reason, need to index second character
		response = response + "\n" + relname[0]
	if (count == 0):
		response = 'Your database is empty. Modify initialization.sql to manually insert values, or import data from another database'
	connection.close()
	return HttpResponse(response, content_type = 'text/plain')

# Get the eastings in the database
def get_area_eastings(request):
	connection = psycopg2.connect(host = hostname, user = username, password = password, dbname = database)
	cursor = connection.cursor()
	cursor.execute("SELECT area_easting FROM Samples WHERE status = 'active' ORDER BY area_easting ASC;")
	response = '<h3>Eastings</h3>\n<ul>'
	for easting in cursor.fetchall():
		# Python thinks this is a tuple of 1 element
		eastingString = str(easting[0])
		response = response + "\n<li><a href = '/get_area_northings/" + eastingString + "'>" + eastingString + "</a></li>"
	response = response + "\n</ul>"
	connection.close()
	return HttpResponse(response, content_type = 'text/html')

# Get the northings under a particular easting
def get_area_northings(request, easting):
	connection = psycopg2.connect(host = hostname, user = username, password = password, dbname = database)
	cursor = connection.cursor()
	eastingString = str(easting)
	cursor.execute("SELECT area_northing FROM Samples WHERE status = 'active' AND area_northing = " + eastingString + " ORDER BY area_easting ASC;")
	response = '<h3>Northings</h3>\n<ul>'
	for northing in cursor.fetchall():
		northingString = str(northing)
		# Python thinks this is a tuple of 1 element
		response = response + "\n<li><a href = '/get_area_contexts/" + eastingString + "/" + northingString + "'>" + eastingString + "." + northingString + "</a></li>"
	response = response + "\n</ul>"
	connection.close()
	return HttpResponse(response, content_type = 'text/plain')