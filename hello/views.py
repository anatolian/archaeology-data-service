# Simple webapp views for Archaeology Django service
# Author: Christopher Besser
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.db import transaction
from django.template import RequestContext
from django import forms
from django.views.decorators.csrf import csrf_exempt
import psycopg2
import os, json, boto3
import logging
import math
logger = logging.getLogger('testlogger')
# For local deployment, these should be defined in system environment variables.
# For Heroku deployment, these must be set in the configuration
hostname = os.environ['postgres-hostname']
username = os.environ['postgres-username']
password = os.environ['postgres-password']
database = os.environ['postgres-database']
AWS_QUERYSTRING_AUTH = False
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_STORAGE_BUCKET_NAME = os.environ['S3_BUCKET_NAME']
MEDIA_URL = 'http://%s.s3.amazonaws.com/images/' % AWS_STORAGE_BUCKET_NAME
DEFAULT_FILE_STORAGE = "storages.backends.s3boto.S3BotoStorage"
# Model for testing that upload_image form is valid
# Param: form - the POST request form
class UploadFileForm(forms.Form):
	hemisphere = forms.CharField(max_length = 1)
	zone = forms.IntegerField(min_value = 0)
	easting = forms.IntegerField(min_value = 0)
	northing = forms.IntegerField(min_value = 0)
	find = forms.IntegerField(min_value = 0)
	file_name = forms.CharField(max_length = 250)
	myFile = forms.FileField()

# Detect SQL keywords in a string
# Param: text - string to search
# Returns the found keyword, if any
def find_sql_keyword(text):
	keywords = [' ALL ', ' ALTER ', ' AND ', ' ANY ', ' ARRAY ', ' ARROW ', ' AS ', ' ASC ', ' AT ', ' BEGIN ', ' BETWEEN ',\
		' BY ', ' CASE ', ' CHECK ', ' CLUSTERS ', ' CLUSTER ', ' COLAUTH ', ' COLUMNS ', ' COMPRESS ', ' CONNECT ', ' CRASH ',\
		' CREATE ', ' CURRENT ', ' DECIMAL ', ' DECLARE ', ' DEFAULT ', ' DELETE ', ' DESC ', ' DISTINCT ', ' DROP ', ' ELSE ',\
		' END ', ' EXCEPTION ', ' EXCLUSIVE ', ' EXISTS ', ' FETCH ', ' FORM ', ' FOR ', ' FROM ', ' GOTO ', ' GRANT ',\
		' GROUP ', ' HAVING ', ' IDENTIFIED ', ' IF ', ' IN ', ' INDEXES ', ' INDEX ', ' INSERT ', ' INTERSECT ', ' INTO ',\
		' IS ', ' LIKE ', ' LOCK ', ' MINUS ', ' MODE ', ' NOCOMPRESS ', ' NOT ', ' NOWAIT ', ' NULL ', ' OF ', ' ON ', ' OPTION ',\
		' OR ', ' ORDER ', ' OVERLAPS ', ' PRIOR ', ' PROCEDURE ', ' PUBLIC ', ' RANGE ', ' RECORD ', ' RESOURCE ', ' REVOKE ',\
		' SELECT ', ' SHARE ', ' SIZE ', ' SQL ', ' START ', ' SUBTYPE ', ' TABAUTH ', ' TABLE ', ' THEN ', ' TO ', ' TYPE ',\
		' UNION ', ' UNIQUE ', ' UPDATE ', ' USE ', ' VALUES ', ' VIEW ', ' VIEWS ', ' WHEN ', ' WHERE ', ' WITH ', ' NATURAL ',\
		' JOIN ', ' INNER ', ' OUTER ']
	for keyword in keywords:
		if (keyword in text.upper()):
			return keyword
	return ''

# Upload a file to Heroku
# Param: request - POST request containing file
# Returns an HTTP response
@csrf_exempt
def upload_file(request):
	# Store file to temporary location then upload to s3
	form = UploadFileForm(request.POST, request.FILES)
	if (form.is_valid()):
		hemisphere = request.POST.get('hemisphere', '')
		zone = request.POST.get('zone', '')
		easting = request.POST.get('easting', '')
		northing = request.POST.get('northing', '')
		find = request.POST.get('find', '')
		file_name = request.POST.get('file_name', '')
		file = request.FILES.get('myFile', '');
		keyword = find_sql_keyword(file_name)
		# The form ensures the other fields must be integers
		if (keyword != ''):
			return HttpResponse('SQL keyword ' + keyword + ' not allowed in file name', content_type = 'text/plain')
		path = hemisphere + "/" + str(zone) + "/" + str(easting) + '/' + str(northing) + '/' + str(find) + '/'
		file_type = file_name[file_name.find('.'):]
		s3 = boto3.resource('s3')
		try:
			# Store the file from multi-part to Heroku Ephemeral File System
			with open('image' + file_type, 'wb+') as destination:
				for chunk in file.chunks():
					destination.write(chunk)
			# Determine correct file name on S3
			imageNumber = 0
			for file in s3.Bucket(AWS_STORAGE_BUCKET_NAME).objects.filter(Prefix = path):
				number = int(file.key[file.key.rfind('/') + 1:file.key.find('.')])
				if (imageNumber < number):
					imageNumber = number
			# Store the image on S3
			path = path + str(imageNumber + 1) + file_type
			data = open('image' + file_type, 'rb')
			s3.Bucket(AWS_STORAGE_BUCKET_NAME).put_object(Key = path, Body = data)
			return HttpResponse("https://s3.amazonaws.com/" + AWS_STORAGE_BUCKET_NAME + "/" + path, 'test/plain')
		except FileNotFoundError:
			return HttpResponse('Error: The file was not saved correctly to Heroku', content_type = 'text/plain')
		except (Exception, boto3.exceptions.S3UploadFailedError) as error:
			return HttpResponse("Error: Insertion failed " + error, content_type = "text/plain")
		except (Exception, botocore.exceptions.ClientError):
			return HttpResponse("Error: Bucket does not exist or credentials are invalid", content_type = 'text/plain')
	else:
		return HttpResponse("Error: Invalid Form", content_type = 'text/plain')

# Route for fetching image urls
# Param request - HTTP client request
# Returns an HTTP response
def get_image_urls(request):
	hemisphere = request.GET.get('hemisphere', '')
	zone = request.GET.get('zone', '')
	easting = request.GET.get('easting', '')
	northing = request.GET.get('northing', '')
	find = request.GET.get('find', '')
	if (len(hemisphere) != 1):
		return HttpResponse('Error: Invalid parameter', content_type = 'text/plain')
	try:
		int(easting)
		int(northing)
		int(find)
	except ValueError:
		return HttpResponse('Error: Invalid parameter', content_type = 'text/plain')
	s3 = boto3.resource('s3')
	path = hemisphere + "/" + zone + "/" + easting + '/' + northing + '/' + find + '/'
	response = '<h3>Image URLs:</h3><ul>'
	found = False
	try:
		for file in s3.Bucket(AWS_STORAGE_BUCKET_NAME).objects.filter(Prefix = path):
			response = response + "<li><a href = 'https://s3.amazonaws.com/" + AWS_STORAGE_BUCKET_NAME + "/" + file.key + "'>"
			response = response + file.key + "</a></li>"
			found = True
		response = response + "</ul>"
		if (not found):
			return HttpResponse('<h3>Error: No images found</h3>', 'text/html')
		return HttpResponse(response, 'text/html')
	except (Exception, botocore.exceptions.ClientError):
		return HttpResponse("Error: Bucket does not exist or credentials are invalid", content_type = 'text/plain')

# Main page
# Param: request - HTTP client request
# Returns an HTML render
def index(request):
	return render(request, 'index.html')

# Get the relation names in the database
# Param: request - HTTP client request
# Returns an HTTP response
def test_connection(request):
	connection = psycopg2.connect(host = hostname, user = username, password = password, dbname = database)
	cursor = connection.cursor()
	cursor.execute("SELECT relname FROM pg_stat_user_tables WHERE schemaname = 'finds';")
	found = False
	# Just looking to see there is something here
	for relname in cursor.fetchall():
		found = True
	cursor.close()
	connection.close()
	if (not found):
		return HttpResponse("Error: No tables found", content_type = 'text/plain')
	s3 = boto3.resource('s3')
	try:
		s3.Bucket(AWS_STORAGE_BUCKET_NAME).objects.all()
		return HttpResponse("Connected to S3", content_type = 'text/plain')
	except (Exception, botocore.exceptions.ClientError):
		return HttpResponse("Error: S3 Bucket does not exist or credentials are invalid", content_type = 'text/plain')
	return HttpResponse("Connections Established", content_type = 'text/plain')

# Get the hemispheres from the database
# Param: request - HTTP request
# Returns an HTTP response
def get_hemispheres(request):
	connection = psycopg2.connect(host = hostname, user = username, password = password, dbname = database)
	cursor = connection.cursor()
	cursor.execute("SELECT DISTINCT utm_hemisphere FROM finds.finds ORDER BY utm_hemisphere ASC;")
	response = '<h3>Hemispheres:</h3><ul>'
	found = False
	for hemisphere in cursor.fetchall():
		# Python thinks this is a tuple of 1 element
		hemisphereString = str(hemisphere[0])
		response = response + "<li><a href = '/get_zones/?hemisphere=" + hemisphereString + "'>" + hemisphereString + "</a></li>"
		found = True
	response = response + "</ul>"
	if (not found):
		response = '<h3>Error: No hemispheres found in finds table</h3>'
	cursor.close()
	connection.close()
	return HttpResponse(response, content_type = 'text/html')

# Get the zones
# Param: request - HTTP request
# Returns the HTTP response
def get_zones(request):
	hemisphere = request.GET.get('hemisphere', '')
	if (len(hemisphere) != 1):
		return HttpResponse("</h3>Error: hemisphere is not a character</h3>", content_type = 'text/html')
	connection = psycopg2.connect(host = hostname, user = username, password = password, dbname = database)
	cursor = connection.cursor()
	cursor.execute("SELECT DISTINCT utm_zone FROM finds.finds WHERE utm_hemisphere = \'" + hemisphere + "\' ORDER BY utm_zone ASC;")
	response = '<h3>Zones:</h3><ul>'
	found = False
	for zone in cursor.fetchall():
		# Python thinks this is a tuple of 1 element
		zoneString = str(zone[0])
		response = response + "<li><a href = '/get_eastings/?hemisphere=" + hemisphere + "&zone=" + zoneString + "'>"
		response = response + hemisphere + "." + zoneString + "</a></li>"
		found = True
	response = response + "</ul>"
	if (not found):
		response = '<h3>Error: No zones found in finds table</h3>'
	cursor.close()
	connection.close()
	return HttpResponse(response, content_type = 'text/html')

# Get the eastings in the database
# Param: request - HTTP client request
# Returns an HTTP response
def get_eastings(request):
	hemisphere = request.GET.get('hemisphere', '')
	zone = request.GET.get('zone', '')
	if (len(hemisphere) != 1):
		return HttpResponse("<h3>Error: hemisphere is not a character</h3>", content_type = 'text/html')
	try:
		int(zone)
	except ValueError:
		return HttpResponse("<h3>Error: Invalid Parameter</h3>", content_type = 'text/html')
	connection = psycopg2.connect(host = hostname, user = username, password = password, dbname = database)
	cursor = connection.cursor()
	query = "SELECT DISTINCT context_utm_easting_meters FROM finds.finds WHERE utm_hemisphere = \'" + hemisphere
	query = query + "\' AND utm_zone = " + zone + " ORDER BY context_utm_easting_meters ASC;"
	cursor.execute(query)
	response = '<h3>Eastings:</h3><ul>'
	found = False
	for easting in cursor.fetchall():
		# Python thinks this is a tuple of 1 element
		eastingString = str(easting[0])
		response = response + "<li><a href = '/get_northings/?hemisphere=" + hemisphere + "&zone=" + zone
		response = response + "&easting=" + eastingString + "'>" + hemisphere + "." + zone
		response = response + "." + eastingString + "</a></li>"
		found = True
	response = response + "</ul>"
	if (not found):
		response = '<h3>Error: No eastings found in finds table</h3>'
	cursor.close()
	connection.close()
	return HttpResponse(response, content_type = 'text/html')

# Get the northings under a particular easting
# Param: request - HTTP client request
# Returns an HTTP response
def get_northings(request):
	easting = request.GET.get('easting', '')
	hemisphere = request.GET.get('hemisphere', '')
	zone = request.GET.get('zone', '')
	if (len(hemisphere) != 1):
		return HttpResponse("<h3>Error: hemisphere is not a character</h3>", content_type = 'text/html')
	try:
		int(zone)
		int(easting)
	except ValueError:
		return HttpResponse("<h3>Error: Invalid Parameter</h3>", content_type = 'text/html')
	connection = psycopg2.connect(host = hostname, user = username, password = password, dbname = database)
	cursor = connection.cursor()
	query = "SELECT DISTINCT context_utm_northing_meters FROM finds.finds WHERE utm_hemisphere = \'" + hemisphere
	query = query + "\' AND utm_zone = " + zone + " AND context_utm_easting_meters = " + easting
	query = query + " ORDER BY context_utm_northing_meters ASC;"
	cursor.execute(query)
	response = '<h3>Northings:</h3><ul>'
	found = False
	for northing in cursor.fetchall():
		# Python thinks this is a tuple of 1 element
		northingString = str(northing[0])
		response = response + "<li><a href = '/get_finds/?hemisphere=" + hemisphere + "&zone=" + zone + "&easting="
		response = response + easting + "&northing=" + northingString + "'>" + hemisphere + "." + zone + "."
		response = response + easting + "." + northingString + "</a></li>"
		found = True
	response = response + "</ul>"
	if (not found):
		response = '<h3>Error: No northings found</h3>'
	cursor.close()
	connection.close()
	return HttpResponse(response, content_type = 'text/html')

# Get find numbers within an easting and northing
# Param: request - HTTP client request
# Returns an HTTP response
def get_finds(request):
	easting = request.GET.get('easting', '')
	northing = request.GET.get('northing', '')
	hemisphere = request.GET.get('hemisphere', '')
	zone = request.GET.get('zone', '')
	if (len(hemisphere) != 1):
		return HttpResponse("<h3>Error: hemisphere is not a character</h3>", content_type = 'text/html')
	try:
		int(zone)
		int(easting)
		int(northing)
	except ValueError:
		return HttpResponse("<h3>Error: Invalid Parameter</h3>", content_type = 'text/html')
	connection = psycopg2.connect(host = hostname, user = username, password = password, dbname = database)
	cursor = connection.cursor()
	query = "SELECT find_number FROM finds.finds WHERE utm_hemisphere = \'" + hemisphere + "\' AND utm_zone = " + zone
	query = query + " AND context_utm_easting_meters = " + easting + " AND context_utm_northing_meters = " + northing
	query = query + " ORDER BY find_number ASC;"
	cursor.execute(query)
	response = '<h3>Find Numbers:</h3><ul>'
	found = False
	for find in cursor.fetchall():
		# Python thinks this is a tuple of 1 element
		findString = str(find[0])
		response = response + "<li><a href = '/get_find/?hemisphere=" + hemisphere + "&zone=" + zone + "&easting="
		response = response + easting + "&northing=" + northing + "&find=" + findString + "'>" + hemisphere + "." + zone
		response = response + "." + easting + "." + northing + "." + findString + "</a></li>"
		found = True
	response = response + "</ul>"
	if (not found):
		response = '<h3>Error: No finds found</h3>'
	cursor.close()
	connection.close()
	return HttpResponse(response, content_type = 'text/html')

# Get a find from the database
# Param: request - HTTP client request
# Returns an HTTP response
def get_find(request):
	hemisphere = request.GET.get('hemisphere', '')
	zone = request.GET.get('zone', '')
	easting = request.GET.get('easting', '')
	northing = request.GET.get('northing', '')
	find = request.GET.get('find', '')
	if (len(hemisphere) != 1):
		return HttpResponse("<h3>Error: hemisphere is not a character</h3>", content_type = 'text/html')
	try:
		int(zone)
		int(easting)
		int(northing)
		int(find)
	except ValueError:
		return HttpResponse("<h3>Error: Invalid Parameter</h3>", content_type = 'text/html')
	connection = psycopg2.connect(host = hostname, user = username, password = password, dbname = database)
	cursor = connection.cursor()
	query = "SELECT * FROM finds.finds WHERE utm_hemisphere = \'" + hemisphere + "\' AND utm_zone = " + zone
	query = query + " AND context_utm_easting_meters = " + easting + " AND context_utm_northing_meters = " + northing
	query = query + " AND find_number = " + find + ";"
	cursor.execute(query)
	response = 'longitude_decimal_degrees | latitude_decimal_degrees | utm_easting_meters | utm_northing_meters '
	response = response + '| material_general | material_specific | category_general | category_specific | weight_kilograms'
	found = False
	for findEntry in cursor.fetchall():
		response = response + "\n" + str(findEntry[5])
		# Skipping primary keys
		for i in range(6, 14):
			response = response + " | " + str(findEntry[i])
		found = True
	if (not found):
		response = 'Error: No finds found'
	cursor.close()
	connection.close()
	return HttpResponse(response, content_type = 'text/plain')

# Get colors from the database
# Param: request - HTTP client request
# Returns an HTTP response
def get_find_colors(request):
	hemisphere = request.GET.get('hemisphere', '')
	zone = request.GET.get('zone', '')
	easting = request.GET.get('easting', '')
	northing = request.GET.get('northing', '')
	location = request.GET.get('location', '')
	locationSQL = find_sql_keyword(location)
	find = request.GET.get('find', '')
	if (len(hemisphere) != 1):
		return HttpResponse("<h3>Error: hemisphere is not a character</h3>", content_type = 'text/html')
	elif (locationSQL != ''):
		return HttpResponse("<h3>Error: SQL keyword in location</h3>", content_type = 'text/html')
	try:
		int(zone)
		int(easting)
		int(northing)
		int(find)
	except ValueError:
		return HttpResponse("<h3>Error: Invalid Parameter</h3>", content_type = 'text/html')
	connection = psycopg2.connect(host = hostname, user = username, password = password, dbname = database)
	cursor = connection.cursor()
	query = "SELECT * FROM finds.finds_colors WHERE utm_hemisphere = \'" + hemisphere + "\' AND utm_zone = " + zone
	query = query + " AND context_utm_easting_meters = " + easting + " AND context_utm_northing_meters = "
	query = query + northing + " AND find_number = " + find + " AND color_location = \'" + location + "\';"
	cursor.execute(query)
	response = 'munsell_hue_number | munsell_hue_letter | munsell_lightness_value | munsell_chroma |'
	response = response + ' rgb_red_256_bit | rgb_green_256_bit | rgb_blue_256_bit'
	found = False
	for findEntry in cursor.fetchall():
		response = response + "\n" + str(findEntry[6])
		# Skipping primary keys
		for i in range(7, 13):
			response = response + " | " + str(findEntry[i])
		found = True
	if (not found):
		response = 'Error: find not found'
	cursor.close()
	connection.close()
	return HttpResponse(response, content_type = 'text/plain')

# Set the weight of an object
# Param: request - HTTP client request
# Returns an HTTP response
def set_weight(request):
	hemisphere = request.GET.get('hemisphere', '')
	zone = request.GET.get('zone', '')
	easting = request.GET.get('easting', '')
	northing = request.GET.get('northing', '')
	find = request.GET.get('find', '')
	weight = request.GET.get('weight', '')
	if (len(hemisphere) != 1):
		return HttpResponse("<h3>Error: hemisphere is not a character</h3>", content_type = 'text/html')
	try:
		int(zone)
		int(easting)
		int(northing)
		int(find)
		float(weight)
	except ValueError:
		return HttpResponse("Error: One or more parameters are invalid", content_type = 'text/plain')
	connection = psycopg2.connect(host = hostname, user = username, password = password, dbname = database)
	cursor = connection.cursor()
	query = "UPDATE finds.finds SET weight_kilograms = " + weight + " WHERE utm_hemisphere = \'" + hemisphere + "\' AND utm_zone = "
	query = query + zone + " AND context_utm_easting_meters = " + easting + " AND context_utm_northing_meters = " + northing
	query = query + " AND find_number = " + find + ';'
	response = None
	try:
		cursor.execute(query)
		# Make sure the query updated a row
		if (cursor.rowcount == 1):
			response = HttpResponse("Update successful", content_type = 'text/plain')
		connection.commit()
	except (Exception, psycopg2.DatabaseError) as error:
		response = HttpResponse("Error: Object not found in finds table", content_type = "text/plain")
	finally:
		cursor.close()
		connection.close()
		return response

# Add a key-value pair to the properties table
# Param: request - HTTP client request
# Returns an HTTP response
def add_property(request):
	key = request.GET.get('key', '')
	value = request.GET.get('value', '')
	keySQL = find_sql_keyword(key)
	valueSQL = find_sql_keyword(value)
	if (len(key) == 0 or keySQL != ''):
		return HttpResponse("Error: key cannot be empty or contain SQL keywords", content_type = 'text/plain')
	elif (len(value) == 0 or valueSQL != ''):
		return HttpResponse("Error: value cannot be empty or contain SQL keywords", content_type = 'text/plain')
	connection = psycopg2.connect(host = hostname, user = username, password = password, dbname = database)
	cursor = connection.cursor()
	query = "INSERT INTO options.procedure_properties VALUES (\'" + key + "\', \'" + value + "\');"
	response = None
	try:
		cursor.execute(query)
		# Make sure the query updated a row
		if (cursor.rowcount == 1):
			response = HttpResponse("Update successful", content_type = 'text/plain')
		connection.commit()
	except (Exception, psycopg2.DatabaseError) as error:
		query = "UPDATE options.procedure_properties SET property_value = \'" + value + "\' WHERE property_name = \'" + key + "\';"
		connection.rollback()
		try:
			cursor.execute(query)
			# Make sure the query updated a row
			if (cursor.rowcount == 1):
				response = HttpResponse("Update successful", content_type = 'text/plain')
			connection.commit()
		except (Exception, psycopg2.DatabaseError) as error2:
			response = HttpResponse("Error: Insertion failed " + error2.pgerror, content_type = "text/plain")
	finally:
		cursor.close()
		connection.close()
		return response

# Get a property from the Properties table
# Param: request - HTTP client Request
# Returns an HTTP response
def get_property(request):
	key = request.GET.get('key', '')
	keyword = find_sql_keyword(key)
	if (len(key) == 0 or keyword != ''):
		return HttpResponse("Error: key cannot be empty or contain SQL keyword", content_type = 'text/plain')
	connection = psycopg2.connect(host = hostname, user = username, password = password, dbname = database)
	cursor = connection.cursor()
	query = "SELECT property_value FROM options.procedure_properties WHERE property_name = \'" + key + "\';"
	cursor.execute(query)
	# There should only be one element in this cursor
	for values in cursor.fetchall():
		cursor.close()
		connection.close()
		return HttpResponse(str(values[0]), content_type = 'text/plain')
	# If these lines are reached then the property must not exist
	cursor.close()
	connection.close()
	return HttpResponse("Error: Property not found", content_type = 'text/plain')

# Get the next item id
# Param: request - HTTP request
# Returns an HTTP response
def get_next_find_id(request):
	hemisphere = request.GET.get('hemisphere', '')
	zone = request.GET.get('zone', '')
	easting = request.GET.get('easting', '')
	northing = request.GET.get('northing', '')
	find = request.GET.get('find', '')
	if (len(hemisphere) != 1):
		return HttpResponse("<h3>Error: hemisphere is not a character</h3>", content_type = 'text/html')
	try:
		int(easting)
		int(northing)
		int(find)
		int(zone)
	except ValueError:
		return HttpResponse("Error: One or more parameters are invalid", content_type = 'text/plain')
	connection = psycopg2.connect(host = hostname, user = username, password = password, dbname = database)
	cursor = connection.cursor()
	query = "SELECT utm_hemisphere, utm_zone, context_utm_easting_meters, context_utm_northing_meters, find_number"
	query = query + " FROM finds.finds ORDER BY utm_hemisphere ASC, utm_zone ASC, context_utm_easting_meters ASC,"
	query = query + " context_utm_northing_meters ASC, find_number ASC;"
	cursor.execute(query)
	# Just return the first
	for values in cursor.fetchall():
		if (values[2] < int(easting)):
			continue;
		elif (values[2] == int(easting) and values[3] < int(northing)):
			continue;
		if (values[2] == int(easting) and values[3] == int(northing) and values[4] <= int(find)):
			continue;
		response = values[0] + "." + str(values[1]) + "." + str(values[2]) + "." + str(values[3]) + "." + str(values[4])
		return HttpResponse(response, content_type = "text/plain")
	cursor.close()
	connection.close()
	# If nothing is found, return the find
	return HttpResponse(hemisphere + "." + zone + "." + easting + "." + northing + "." + find, content_type = "text/plain");

# Get the next item id
# Param: request - HTTP request
# Returns an HTTP response
def get_previous_find_id(request):
	hemisphere = request.GET.get('hemisphere', '')
	zone = request.GET.get('zone', '')
	easting = request.GET.get('easting', '')
	northing = request.GET.get('northing', '')
	find = request.GET.get('find', '')
	if (len(hemisphere) != 1):
		return HttpResponse("<h3>Error: hemisphere is not a character</h3>", content_type = 'text/html')
	try:
		int(easting)
		int(northing)
		int(find)
		int(zone)
	except ValueError:
		return HttpResponse("Error: One or more parameters are invalid", content_type = 'text/plain')
	connection = psycopg2.connect(host = hostname, user = username, password = password, dbname = database)
	cursor = connection.cursor()
	query = "SELECT utm_hemisphere, utm_zone, context_utm_easting_meters, context_utm_northing_meters, find_number"
	query = query + " FROM finds.finds ORDER BY utm_hemisphere DESC, utm_zone DESC, context_utm_easting_meters DESC,"
	query = query + " context_utm_northing_meters DESC, find_number DESC;"
	cursor.execute(query)
	# Just return the first
	for values in cursor.fetchall():
		if (values[2] > int(easting)):
			continue;
		elif (values[2] == int(easting) and values[3] > int(northing)):
			continue;
		if (values[2] == int(easting) and values[3] == int(northing) and values[4] >= int(find)):
			continue;
		response = values[0] + "." + str(values[1]) + "." + str(values[2]) + "." + str(values[3]) + "." + str(values[4])
		return HttpResponse(response, content_type = "text/plain")
	cursor.close()
	connection.close()
	# If nothing is found, return the find
	return HttpResponse(hemisphere + "." + zone + "." + easting + "." + northing + "." + find, content_type = "text/plain");

# Update the item's color
# Param: request - HTTP request
# Returns an HTTP response
def set_color(request):
	hemisphere = request.GET.get('hemisphere', '')
	zone = request.GET.get('zone', '')
	easting = request.GET.get("easting", "");
	northing = request.GET.get("northing", "");
	find = request.GET.get("find", "");
	red = request.GET.get("red", "");
	green = request.GET.get("green", "");
	blue = request.GET.get("blue", "");
	location = request.GET.get("location", "");
	if (len(hemisphere) != 1):
		return HttpResponse("<h3>Error: hemisphere is not a character</h3>", content_type = 'text/html')
	try:
		int(easting)
		int(northing)
		int(find)
		int(red)
		int(green)
		int(blue)
		int(zone)
	except ValueError:
		return HttpResponse("Error: One or more parameters are invalid", content_type = 'text/plain');
	newRed = int(red)
	newGreen = int(green)
	newBlue = int(blue)
	keyword = find_sql_keyword(location)
	if (len(location) == 0 or keyword != ''):
		return HttpResponse("Error: location cannot be empty or contain SQL keyword", content_type = 'text/plain')
	connection = psycopg2.connect(host = hostname, user = username, password = password, dbname = database)
	cursor = connection.cursor()
	query = "SELECT * FROM options.munsell_colors WHERE rgb_red_256_bit IS NOT NULL AND rgb_green_256_bit IS NOT NULL"
	query = query + " AND rgb_blue_256_bit IS NOT NULL;"
	cursor.execute(query)
	minDistance = 999999999.0
	closest = []
	for color in cursor.fetchall():
		# Python thinks this is a tuple of 1 element
		redByte = int(color[4])
		greenByte = int(color[5])
		blueByte = int(color[6])
		distance = math.pow(newRed - redByte, 2) + math.pow(newGreen - greenByte, 2) + math.pow(newBlue - blueByte, 2)
		if (distance < minDistance):
			minDistance = distance
			closest = color
	query = "INSERT INTO finds.finds_colors VALUES (\'" + hemisphere + "\', " + zone + ", " + easting + ", " + northing + ", "
	query = query + find + ", \'" + location + "\', " + str(closest[0]) + ", \'" + closest[1] + "\', " + str(closest[2]) + ", "
	query = query + str(closest[3]) + ", " + red + ", " + green + ", " + blue + ");"
	response = HttpResponse("Error: No records updated\n" + query, content_type = 'text/plain')
	try:
		cursor.execute(query)
		# Make sure the query updated a row
		if (cursor.rowcount == 1):
			response = HttpResponse("Update successful", content_type = 'text/plain')
		connection.commit()
	except (Exception, psycopg2.DatabaseError) as error:
		query2 = "UPDATE finds.finds_colors SET munsell_hue_number = " + str(closest[0]) + ", munsell_hue_letter = \'" + closest[1] + "\',"
		query2 = query2 + " munsell_lightness_value = " + str(closest[2]) + ", munsell_chroma = " + closest[3] + ", rgb_red_256_bit = "
		query2 = query2 + green + ", rgb_blue_256_bit = " + blue + " WHERE utm_hemisphere = \'" + hemisphere + "\' AND utm_zone = "
		query2 = query2 + red + ", rgb_green_256_bit = " + zone + " AND context_utm_easting_meters = " + easting + " AND context_utm_northing_meters = "
		query2 = query2 + northing + " AND find_number = " + find + " AND color_location = \'" + location + "\';"
		connection.rollback()
		try:
			cursor.execute(query2)
			# Make sure the query updated a row
			if (cursor.rowcount == 1):
				response = HttpResponse("Update successful", content_type = 'text/plain')
			connection.commit()
		except (Exception, psycopg2.DatabaseError) as error2:
			response = "Error: Update failed \n" + query + "\n" + error.pgerror + "\n" + query2 + "\n" + error2.pgerror
			response = HttpResponse(response, content_type = "text/plain")
	finally:
		cursor.close()
		connection.close()
		return response
		
# Add an item
# Param: request - HTTP request
# Returns an HTTP response
def insert_find(request):
	zone = request.GET.get("zone", "");
	hemisphere = request.GET.get("hemisphere", "");
	easting = request.GET.get("easting", "");
	northing = request.GET.get("northing", "");
	find = request.GET.get("find", "");
	contextEasting = request.GET.get("contextEasting", "");
	contextNorthing = request.GET.get("contextNorthing", "");
	latitude = request.GET.get("latitude", "");
	longitude = request.GET.get("longitude", "");
	altitude = request.GET.get("altitude", "");
	status = request.GET.get("status", "");
	material = request.GET.get("material", ""); #not used 
	comments = request.GET.get("comments", "");
	ARratio = request.GET.get("ARratio", "");
	if (len(hemisphere) != 1):
		return HttpResponse("<h3>Error: hemisphere is not a character</h3>", content_type = 'text/html')
	try:
		int(zone)
		int(easting)
		int(northing)
		float(contextEasting) #TODO: make this int
		float(contextNorthing) #TODO: make this int
		int(find)
		float(latitude)
		float(longitude)
		float(ARratio)
	except ValueError:
		return HttpResponse("Error: One or more parameters are invalid", content_type = 'text/plain');
	status = status.lower()
	if (find_sql_keyword(comments) != ''):
		return HttpResponse("Error: comments cannot contain SQL keyword", content_type = 'text/plain')
	connection = psycopg2.connect(host = hostname, user = username, password = password, dbname = database)
	cursor = connection.cursor()
	query = "INSERT INTO finds.finds (utm_zone, utm_hemisphere, utm_easting_meters, utm_northing_meters, find_number, "
	query = query + "latitude_decimal_degrees, longitude_decimal_degrees, utm_altitude, position_recording_status, position_recording_ar_ratio, field_comments, context_utm_easting_meters, context_utm_northing_meters, material_general) VALUES (" + zone + ", \'" + hemisphere
	query = query + "\', " + easting + ", " + northing + ", " + find + ", " + latitude + ", " + longitude + ", " + altitude + ", \'" + status.lower() + "\', " + ARratio + ", \'" + comments + "\', " + contextEasting + ", " + contextNorthing + ", \'" + material + "\');"
	response = HttpResponse("Error: No records updated\n" + query, content_type = 'text/plain')
	try:
		cursor.execute(query)
		# Make sure the query updated a row
		if (cursor.rowcount == 1):
			response = HttpResponse("Update successful", content_type = 'text/plain')
		connection.commit()
	except (Exception, psycopg2.DatabaseError) as error:
		response = HttpResponse("Error: Update failed\n" + error.pgerror, content_type = "text/plain")
	finally:
		cursor.close()
		connection.close()
		return response
		
# Add a path
# Param: request - HTTP request
# Returns an HTTP response
def insert_path(request):
	teamMember = request.GET.get("teamMember", "");
	zone = request.GET.get("zone", "");
	hemisphere = request.GET.get("hemisphere", "");
	beginEasting = request.GET.get("beginEasting", "");
	beginNorthing = request.GET.get("beginNorthing", "");
	beginLatitude = request.GET.get("beginLatitude", "");
	beginLongitude = request.GET.get("beginLongitude", "");
	beginAltitude = request.GET.get("beginAltitude", "");
	beginStatus = request.GET.get("beginStatus", "");
	beginARRatio = request.GET.get("beginARRatio", "");
	beginTime = request.GET.get("beginTime", "");
	endEasting = request.GET.get("endEasting", "");
	endNorthing = request.GET.get("endNorthing", "");
	endLatitude = request.GET.get("endLatitude", "");
	endLongitude = request.GET.get("endLongitude", "");
	endAltitude = request.GET.get("endAltitude", "");
	endStatus = request.GET.get("endStatus", "");
	endARRatio = request.GET.get("endARRatio", "");
	endTime = request.GET.get("endTime", "");
	if (len(hemisphere) != 1):
		return HttpResponse("<h3>Error: hemisphere is not a character</h3>", content_type = 'text/html')
	try:
		int(zone)
		float(beginEasting)
		float(beginNorthing)
		float(beginLatitude)
		float(beginLongitude)
		float(beginAltitude)
		float(beginARRatio)
		float(endEasting)
		float(endNorthing)
		float(endLatitude)
		float(endLongitude)
		float(endAltitude)
		float(endARRatio)
		float(beginTime)
		float(endTime)
	except ValueError:
		return HttpResponse("Error: One or more parameters are invalid", content_type = 'text/plain');
	beginStatus = beginStatus.lower()
	endStatus = endStatus.lower()
	connection = psycopg2.connect(host = hostname, user = username, password = password, dbname = database)
	cursor = connection.cursor()
	query = "INSERT INTO survey.tracks (team_member, utm_hemisphere, utm_zone, begin_utm_easting_meters, begin_utm_northing_meters, end_utm_easting_meters, "
	query = query + "end_utm_northing_meters, begin_longitude_decimal_degrees, begin_latitude_decimal_degrees, begin_altitude_meters, begin_position_recording_status, "
	query = query + "begin_position_recording_ar_ratio, end_longitude_decimal_degrees, end_latitude_decimal_degrees, end_altitude_meters, end_position_recording_status, "
	query = query + "end_position_recording_ar_ratio, begin_timestamp, end_timestamp) VALUES (\'" + teamMember + "\', \'" + hemisphere + "\', " + zone + ", " + beginEasting
	query = query + ", " + beginNorthing + ", " + endEasting + ", " + endNorthing + ", " + beginLongitude + ", " + beginLatitude + ", " + beginAltitude + ", \'" 
	query = query + beginStatus + "\', " + beginARRatio + ", " + endLongitude + ", " + endLatitude + ", " + endAltitude + ", \'" + endStatus + "\', " + endARRatio
	query = query + ", to_timestamp(\'" + beginTime + "\' AS DOUBLE PRECISION), to_timestamp(\'" + endTime + "\') AS DOUBLE PRECISION);"
	response = HttpResponse("Error: No records updated\n" + query, content_type = 'text/plain')
	try:
		cursor.execute(query)
		# Make sure the query updated a row
		if (cursor.rowcount == 1):
			response = HttpResponse("Update successful", content_type = 'text/plain')
		connection.commit()
	except (Exception, psycopg2.DatabaseError) as error:
		response = HttpResponse("Error: Update failed\n" + error.pgerror, content_type = "text/plain")
	finally:
		cursor.close()
		connection.close()
		return response
		
		
# Get the team members from the database
# Param: request - HTTP request
# Returns an HTTP response
def get_team_members(request):
	connection = psycopg2.connect(host = hostname, user = username, password = password, dbname = database)
	cursor = connection.cursor()
	cursor.execute("SELECT DISTINCT team_member FROM options.team_members ORDER BY team_member ASC;")
	response = ''
	found = False;
	for teamMember in cursor.fetchall():
		# Python thinks this is a tuple of 1 element
		teamMemberString = str(teamMember[0])
		response = response + teamMemberString + "\n"
		found = True
	if (not found):
		response = 'Error: No team members found in the options database'
	cursor.close()
	connection.close()
	return HttpResponse(response, content_type = 'text/plain')
	
	
# Get the materials from the database
# Param: request - HTTP request
# Returns an HTTP response
def get_material_generals(request):
	connection = psycopg2.connect(host = hostname, user = username, password = password, dbname = database)
	cursor = connection.cursor()
	cursor.execute("SELECT DISTINCT material_general FROM options.materials ORDER BY material_general ASC;")
	response = ''
	found = False;
	for material in cursor.fetchall():
		# Python thinks this is a tuple of 1 element
		materialString = str(material[0])
		response = response + materialString + "\n"
		found = True
	if (not found):
		response = 'Error: No general materials found in the options database'
	cursor.close()
	connection.close()
	return HttpResponse(response, content_type = 'text/plain')
	
