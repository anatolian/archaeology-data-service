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
	found = False
	for relname in cursor.fetchall():
		found = True
		# Python thinks this is a tuple of 1 element
		response = response + "\n" + relname[0]
	if (not found):
		response = 'Your database is empty. Modify initialization.sql to manually insert values, or import data from another database'
	connection.close()
	return HttpResponse(response, content_type = 'text/plain')

# Get the eastings in the database
def get_area_eastings(request):
	connection = psycopg2.connect(host = hostname, user = username, password = password, dbname = database)
	cursor = connection.cursor()
	cursor.execute("SELECT area_easting FROM Samples WHERE status = 'active' ORDER BY area_easting ASC;")
	response = '<h3>Area Eastings:</h3><ul>'
	found = False
	for easting in cursor.fetchall():
		# Python thinks this is a tuple of 1 element
		eastingString = str(easting[0])
		response = response + "<li><a href = '/get_area_northings/?easting=" + eastingString + "'>" + eastingString + "</a></li>"
		found = True
	response = response + "</ul>"
	if (not found):
		response = '<h3>Error: No area_eastings found in Samples table</h3>'
	connection.close()
	return HttpResponse(response, content_type = 'text/html')

# Get the northings under a particular easting
def get_area_northings(request):
	connection = psycopg2.connect(host = hostname, user = username, password = password, dbname = database)
	cursor = connection.cursor()
	easting = request.GET.get('easting', '')
	try:
		int(easting)
	except ValueError:
		return HttpResponse('<h3>Provided area_easting is not a number</h3>', content_type = 'text/html')
	cursor.execute("SELECT area_northing FROM Samples WHERE status = 'active' AND area_easting = '" + easting + "' ORDER BY area_northing ASC;")
	response = '<h3>Area Northings:</h3><ul>'
	found = False
	for northing in cursor.fetchall():
		# Python thinks this is a tuple of 1 element
		northingString = str(northing[0])
		response = response + "<li><a href = '/get_context_numbers/?easting=" + easting + "&northing=" + northingString + "'>" + easting + "." + northingString + "</a></li>"
		found = True
	response = response + "</ul>"
	if (not found):
		response = '<h3>Error: No area_northings with area_easting = ' + easting + ' found in Samples table</h3>'
	connection.close()
	return HttpResponse(response, content_type = 'text/html')

# Get contexts within an easting and northing
def get_context_numbers(request):
	connection = psycopg2.connect(host = hostname, user = username, password = password, dbname = database)
	cursor = connection.cursor()
	easting = request.GET.get('easting', '')
	northing = request.GET.get('northing', '')
	try:
		int(easting)
	except ValueError:
		return HttpResponse('<h3>Provided area_easting is not a number</h3>', content_type = 'text/html')
	try:
		int(northing)
	except ValueError:
		return HttpResponse('<h3>Provided area_northing is not a number</h3>', content_type = 'text/html')
	query = "SELECT context_number FROM Samples WHERE status = 'active' AND area_easting = '" + easting
	query = query + "' AND area_northing = '" + northing + "' ORDER BY context_number ASC;"
	cursor.execute(query)
	response = '<h3>Context Numbers:</h3><ul>'
	found = False
	for context in cursor.fetchall():
		# Python thinks this is a tuple of 1 element
		contextString = str(context[0])
		response = response + "<li><a href = '/get_sample_numbers/?easting=" + easting + "&northing=" + northing + "&context=" + contextString + "'>"
		response = response + easting + "." + northing + "." + contextString + "</a></li>"
		found = True
	response = response + "</ul>"
	if (not found):
		response = '<h3>Error: No context_numbers with area_easting = ' + easting + ' and area_northing = ' + northing + ' found in Samples table</h3>'
	connection.close()
	return HttpResponse(response, content_type = 'text/html')

# Get sample numbers within an easting, northing, and context
def get_sample_numbers(request):
	connection = psycopg2.connect(host = hostname, user = username, password = password, dbname = database)
	cursor = connection.cursor()
	easting = request.GET.get('easting', '')
	northing = request.GET.get('northing', '')
	context = request.GET.get('context', '')
	try:
		int(easting)
	except ValueError:
		return HttpResponse('<h3>Provided area_easting is not a number</h3>', content_type = 'text/html')
	try:
		int(northing)
	except ValueError:
		return HttpResponse('<h3>Provided area_northing is not a number</h3>', content_type = 'text/html')
	try:
		int(context)
	except ValueError:
		return HttpResponse('<h3>Provided context_number is not a number</h3>', content_type = 'text/html')
	query = "SELECT sample_number FROM Samples WHERE status = 'active' AND area_easting = '" + easting
	query = query + "' AND area_northing = '" + northing + "' AND context_number = '" + context + "' ORDER BY sample_number ASC;"
	cursor.execute(query)
	response = '<h3>Sample Numbers:</h3><ul>'
	found = False
	for sample in cursor.fetchall():
		# Python thinks this is a tuple of 1 element
		sampleString = str(sample[0])
		response = response + "<li><a href = '/get_sample/?easting=" + easting + "&northing=" + northing + "&context=" + context + "&sample=" + sampleString + "'>"
		response = response + easting + "." + northing + "." + context + "." + sampleString + "</a></li>"
		found = True
	response = response + "</ul>"
	if (not found):
		response = '<h3>Error: No sample_numbers with area_easting = ' + easting + ', area_northing = ' + northing
		response = response + ', and context_number = ' + context + ' found in Samples table</h3>'
	connection.close()
	return HttpResponse(response, content_type = 'text/html')

# Get a sample from the database
def get_sample(request):
	connection = psycopg2.connect(host = hostname, user = username, password = password, dbname = database)
	cursor = connection.cursor()
	easting = request.GET.get('easting', '')
	northing = request.GET.get('northing', '')
	context = request.GET.get('context', '')
	sample = request.GET.get('sample', '')
	try:
		int(easting)
	except ValueError:
		return HttpResponse('<h3>Provided area_easting is not a number</h3>', content_type = 'text/html')
	try:
		int(northing)
	except ValueError:
		return HttpResponse('<h3>Provided area_northing is not a number</h3>', content_type = 'text/html')
	try:
		int(context)
	except ValueError:
		return HttpResponse('<h3>Provided context_number is not a number</h3>', content_type = 'text/html')
	try:
		int(sample)
	except ValueError:
		return HttpResponse('<h3>Provided sample_number is not a number</h3>', content_type = 'text/html')
	query = "SELECT * FROM Samples WHERE status = 'active' AND area_easting = '" + easting + "' AND area_northing = '" + northing
	query = query  + "' AND context_number = '" + context + "' AND sample_number = '" + sample + "'"
	cursor.execute(query)
	response = 'material | exterior_color_hue | exterior_color_lightness_value | exterior_color_chroma | interior_color_hue | '
	response = response + 'interior_color_lightness_value | interior_color_chroma | weight_kilograms'
	found = False
	for sampleEntry in cursor.fetchall():
		response = response + "\n" + str(sampleEntry[4])
		# Skipping area_easting, area_northing, context_number, sample_number, and status
		for i in range(5, 12):
			response = response + " | " + str(sampleEntry[i])
		found = True
	if (not found):
		response = 'Error: No samples with area_easting = ' + easting + ', area_northing = ' + northing
		response = response + ', context_number = ' + context + ', and sample_number = ' + sample + ' found in Samples table'
	connection.close()
	return HttpResponse(response, content_type = 'text/plain')