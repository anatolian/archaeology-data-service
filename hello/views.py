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
	easting = forms.IntegerField(min_value = 0)
	northing = forms.IntegerField(min_value = 0)
	find = forms.IntegerField(min_value = 0)
	file_name = forms.CharField(max_length = 250)
	myFile = forms.FileField()

# Detect SQL keywords in a string
# Param: text - string to search
# Returns the found keyword, if any
def find_sql_keyword(text):
	keywords = [' ALL ', ' ALTER ', ' AND ', ' ANY ', ' ARRAY ', ' ARROW ', ' AS ', ' ASC ', ' AT ', ' BEGIN ', ' BETWEEN ', ' BY ', ' CASE ', ' CHECK ',\
		' CLUSTERS ', ' CLUSTER ', ' COLAUTH ', ' COLUMNS ', ' COMPRESS ', ' CONNECT ', ' CRASH ', ' CREATE ', ' CURRENT ', ' DECIMAL ', ' DECLARE ',\
		' DEFAULT ', ' DELETE ', ' DESC ', ' DISTINCT ', ' DROP ', ' ELSE ', ' END ', ' EXCEPTION ', ' EXCLUSIVE ', ' EXISTS ', ' FETCH ', ' FORM ', ' FOR ',\
		' FROM ', ' GOTO ', ' GRANT ', ' GROUP ', ' HAVING ', ' IDENTIFIED ', ' IF ', ' IN ', ' INDEXES ', ' INDEX ', ' INSERT ', ' INTERSECT ', ' INTO ',\
		' IS ', ' LIKE ', ' LOCK ', ' MINUS ', ' MODE ', ' NOCOMPRESS ', ' NOT ', ' NOWAIT ', ' NULL ', ' OF ', ' ON ', ' OPTION ', ' OR ', ' ORDER ',\
		' OVERLAPS ', ' PRIOR ', ' PROCEDURE ', ' PUBLIC ', ' RANGE ', ' RECORD ', ' RESOURCE ', ' REVOKE ', ' SELECT ', ' SHARE ', ' SIZE ', ' SQL ',\
		' START ', ' SUBTYPE ', ' TABAUTH ', ' TABLE ', ' THEN ', ' TO ', ' TYPE ', ' UNION ', ' UNIQUE ', ' UPDATE ', ' USE ', ' VALUES ', ' VIEW ', ' VIEWS '\
		' WHEN ', ' WHERE ', ' WITH ', ' NATURAL ', ' JOIN ', ' INNER ', ' OUTER ']
	for keyword in keywords:
		if (keyword in text.upper()):
			return keyword
	return ''

# Upload a file to Heroku
# Param: request - POST request containing file
# Returns an HTTP response
@csrf_exempt
def upload_file(request):
	if (request.method == 'POST'):
		# Store file to temporary location then upload to s3
		logger.info('POST Detected')
		form = UploadFileForm(request.POST, request.FILES)
		if (form.is_valid()):
			logger.info('Valid Form')
			easting = request.POST.get('easting', '')
			northing = request.POST.get('northing', '')
			find = request.POST.get('find', '')
			file_name = request.POST.get('file_name', '')
			file = request.FILES.get('myFile', '');
			keyword = find_sql_keyword(file_name)
			# The form ensures the other fields must be integers
			if (keyword != ''):
				return HttpResponse('SQL keyword ' + keyword + ' not allowed in file_name', content_type = 'text/plain')
			path = 'N/35/' + easting + '/' + northing + '/' + find + '/'
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
			logger.info('Invalid Form')
			form = UploadFileForm()
	logger.info('Redirecting request to blank form')
	return render(request, 'upload_image.html', {'form': form})

# Route for fetching image urls
# Param request - HTTP client request
# Returns an HTTP response
def get_image_urls(request):
	easting = request.GET.get('easting', '')
	northing = request.GET.get('northing', '')
	find = request.GET.get('find', '')
	try:
		int(easting)
	except ValueError:
		return HttpResponse('Provided area easting is not a number', content_type = 'text/plain')
	try:
		int(northing)
	except ValueError:
		return HttpResponse('Provided area northing is not a number', content_type = 'text/plain')
	try:
		int(find)
	except ValueError:
		return HttpResponse('Provided find number is not a number', content_type = 'text/plain')
	s3 = boto3.resource('s3')
	path = easting + '/' + northing + '/' + find + '/'
	response = '<h3>Image URLs:</h3><ul>'
	found = False
	try:
		for file in s3.Bucket(AWS_STORAGE_BUCKET_NAME).objects.filter(Prefix = path):
			response = response + "<li><a href = 'https://s3.amazonaws.com/" + AWS_STORAGE_BUCKET_NAME + "/" + file.key + "'>" + file.key + "</a></li>"
			found = True
		response = response + "</ul>"
		if (not found):
			return HttpResponse('<h3>No images found</h3>', 'text/html')
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
	cursor.execute("SELECT relname FROM pg_stat_user_tables WHERE schemaname = 'public';")
	found = False
	# Just looking to see there is something here
	for relname in cursor.fetchall():
		found = True
	cursor.close()
	connection.close()
	if (not found):
		return HttpResponse("Error: No tables found", content_type = 'text/plain')
	# s3 = boto3.resource('s3')
	# try:
	# 	for file in s3.Bucket(AWS_STORAGE_BUCKET_NAME).objects.all():
	# 		return HttpResponse("Connected to S3", content_type = 'text/plain')
	# 	return HttpResponse("Connected to S3, but bucket is empty", content_type = 'text/plain')
	# except (Exception, botocore.exceptions.ClientError):
	# 	return HttpResponse("Error: S3 Bucket does not exist or credentials are invalid", content_type = 'text/plain')
	return HttpResponse("Connections Established", content_type = 'text/plain')

# Get the eastings in the database
# Param: request - HTTP client request
# Returns an HTTP response
def get_eastings(request):
	connection = psycopg2.connect(host = hostname, user = username, password = password, dbname = database)
	cursor = connection.cursor()
	cursor.execute("SELECT DISTINCT context_utm_easting_meters FROM finds ORDER BY context_utm_easting_meters ASC;")
	response = '<h3>Eastings:</h3><ul>'
	found = False
	for easting in cursor.fetchall():
		# Python thinks this is a tuple of 1 element
		eastingString = str(easting[0])
		response = response + "<li><a href = '/get_northings/?easting=" + eastingString + "'>N.35." + eastingString + "</a></li>"
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
	try:
		int(easting)
	except ValueError:
		return HttpResponse('<h3>Provided easting is not a number</h3>', content_type = 'text/html')
	connection = psycopg2.connect(host = hostname, user = username, password = password, dbname = database)
	cursor = connection.cursor()
	cursor.execute("SELECT DISTINCT context_utm_northing_meters FROM finds WHERE context_utm_easting_meters = " + easting + " ORDER BY context_utm_northing_meters ASC;")
	response = '<h3>Northings:</h3><ul>'
	found = False
	for northing in cursor.fetchall():
		# Python thinks this is a tuple of 1 element
		northingString = str(northing[0])
		response = response + "<li><a href = '/get_finds/?easting=" + easting + "&northing=" + northingString + "'>N.35." + easting + "." + northingString + "</a></li>"
		found = True
	response = response + "</ul>"
	if (not found):
		response = '<h3>Error: No northings with easting = ' + easting + ' found in finds table</h3>'
	cursor.close()
	connection.close()
	return HttpResponse(response, content_type = 'text/html')

# Get find numbers within an easting and northing
# Param: request - HTTP client request
# Returns an HTTP response
def get_finds(request):
	easting = request.GET.get('easting', '')
	northing = request.GET.get('northing', '')
	try:
		int(easting)
	except ValueError:
		return HttpResponse('<h3>Provided easting is not a number</h3>', content_type = 'text/html')
	try:
		int(northing)
	except ValueError:
		return HttpResponse('<h3>Provided northing is not a number</h3>', content_type = 'text/html')
	connection = psycopg2.connect(host = hostname, user = username, password = password, dbname = database)
	cursor = connection.cursor()
	query = "SELECT find_number FROM finds WHERE context_utm_easting_meters = " + easting
	query = query + " AND context_utm_northing_meters = " + northing + " ORDER BY find_number ASC;"
	cursor.execute(query)
	response = '<h3>Find Numbers:</h3><ul>'
	found = False
	for find in cursor.fetchall():
		# Python thinks this is a tuple of 1 element
		findString = str(find[0])
		response = response + "<li><a href = '/get_find/?easting=" + easting + "&northing=" + northing + "&find=" + findString + "'>N.35."
		response = response + easting + "." + northing + "." + findString + "</a></li>"
		found = True
	response = response + "</ul>"
	if (not found):
		response = '<h3>Error: No finds with easting = ' + easting + ' and northing = ' + northing + ' found in finds table</h3>'
	cursor.close()
	connection.close()
	return HttpResponse(response, content_type = 'text/html')

# Get a find from the database
# Param: request - HTTP client request
# Returns an HTTP response
def get_find(request):
	easting = request.GET.get('easting', '')
	northing = request.GET.get('northing', '')
	find = request.GET.get('find', '')
	try:
		int(easting)
	except ValueError:
		return HttpResponse('Provided easting is not a number', content_type = 'text/plain')
	try:
		int(northing)
	except ValueError:
		return HttpResponse('Provided northing is not a number', content_type = 'text/plain')
	try:
		int(find)
	except ValueError:
		return HttpResponse('Provided find number is not a number', content_type = 'text/plain')
	connection = psycopg2.connect(host = hostname, user = username, password = password, dbname = database)
	cursor = connection.cursor()
	query = "SELECT * FROM finds WHERE context_utm_easting_meters = " + easting + " AND context_utm_northing_meters = " + northing + " AND find_number = " + find + ";"
	cursor.execute(query)
	response = 'longitude_decimal_degrees | latitude_decimal_degrees | utm_easting_meters | utm_northing_meters | material_general | material_specific | category_general |'
	response = response + ' category_specific | weight_kilograms'
	found = False
	for findEntry in cursor.fetchall():
		response = response + "\n" + str(findEntry[5])
		# Skipping primary keys
		for i in range(6, 14):
			response = response + " | " + str(findEntry[i])
		found = True
	if (not found):
		response = 'Error: No finds with easting = ' + easting + ', northing = ' + northing + ', and find_number = ' + find + ' found in finds table'
	cursor.close()
	connection.close()
	return HttpResponse(response, content_type = 'text/plain')

# Get colors from the database
# Param: request - HTTP client request
# Returns an HTTP response
def get_find_colors(request):
	easting = request.GET.get('easting', '')
	northing = request.GET.get('northing', '')
	location = request.GET.get('location', '')
	locationSQL = find_sql_keyword(location)
	find = request.GET.get('find', '')
	try:
		int(easting)
	except ValueError:
		return HttpResponse('Error: Provided easting is not a number', content_type = 'text/plain')
	try:
		int(northing)
	except ValueError:
		return HttpResponse('Error: Provided northing is not a number', content_type = 'text/plain')
	try:
		int(find)
	except ValueError:
		return HttpResponse('Error: Provided find number is not a number', content_type = 'text/plain')
	if (len(location) == 0 or locationSQL != ""):
		return HttpResponse('Error: Location must be non-empty and not contain SQL keywords', content_type = 'text/plain')
	connection = psycopg2.connect(host = hostname, user = username, password = password, dbname = database)
	cursor = connection.cursor()
	query = "SELECT * FROM finds_colors WHERE context_utm_easting_meters = " + easting + " AND context_utm_northing_meters = " + northing
	query = query + " AND find_number = " + find + " AND color_location = \'" + location + "\';"
	cursor.execute(query)
	response = 'munsell_hue_number | munsell_hue_letter | munsell_lightness_value | munsell_chroma | rgb_red_256_bit | rgb_green_256_bit | rgb_blue_256_bit'
	found = False
	for findEntry in cursor.fetchall():
		response = response + "\n" + str(findEntry[6])
		# Skipping primary keys
		for i in range(7, 13):
			response = response + " | " + str(findEntry[i])
		found = True
	if (not found):
		response = 'Error: No finds with easting = ' + easting + ', northing = ' + northing + ', and find_number = ' + find + ' found in finds table'
	cursor.close()
	connection.close()
	return HttpResponse(response, content_type = 'text/plain')

# Set the weight of an object
# Param: request - HTTP client request
# Returns an HTTP response
def set_weight(request):
	easting = request.GET.get('easting', '')
	northing = request.GET.get('northing', '')
	find = request.GET.get('find', '')
	weight = request.GET.get('weight', '')
	try:
		int(easting)
		int(northing)
		int(find)
		float(weight)
	except ValueError:
		return HttpResponse("Error: One or more parameters are invalid", content_type = 'text/plain')
	connection = psycopg2.connect(host = hostname, user = username, password = password, dbname = database)
	cursor = connection.cursor()
	query = "UPDATE finds SET weight_kilograms = " + weight + " WHERE context_utm_easting_meters = " + easting + " AND context_utm_northing_meters = "
	query = query + northing + " AND find_number = " + find + ';'
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
	query = "INSERT INTO Properties VALUES (\'" + key + "\', \'" + value + "\');"
	response = None
	try:
		cursor.execute(query)
		# Make sure the query updated a row
		if (cursor.rowcount == 1):
			response = HttpResponse("Update successful", content_type = 'text/plain')
		connection.commit()
	except (Exception, psycopg2.DatabaseError) as error:
		query = "UPDATE Properties SET value = \'" + value + "\' WHERE label = \'" + key + "\';"
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
	query = "SELECT value FROM Properties WHERE label = \'" + key + "\';"
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