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
	response = 'area_easting'
	count = 0
	for easting in cursor.fetchall():
		count += 1
		# Python thinks this is a tuple of 1 element
		response = response + "\n" + str(easting[0])
	if (count == 0):
		response = 'Samples relation is empty'
	connection.close()
	return HttpResponse(response, content_type = 'text/plain')