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
class UploadFileForm(forms.Form):
	easting = forms.IntegerField(min_value = 0)
	northing = forms.IntegerField(min_value = 0)
	context = forms.IntegerField(min_value = 0)
	sample = forms.IntegerField(min_value = 0)
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
# Returns an http response
@csrf_exempt
def upload_file(request):
	if (request.method == 'POST'):
		# Store file to temporary location then upload to s3
		logger.info('POST Detected')
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
			logger.info('Valid Form')
			easting = request.POST.get('easting', '')
			northing = request.POST.get('northing', '')
			context = request.POST.get('context', '')
			sample = request.POST.get('sample', '')
			file_name = request.POST.get('file_name', '')
			file = request.FILES.get('myFile', '');
			keyword = find_sql_keyword(file_name)
			# The form ensures the other fields must be integers
			if (keyword != ''):
				return HttpResponse('SQL keyword ' + keyword + ' not allowed in file_name', content_type = 'text/plain')
			file_type = file_name[file_name.find('.'):]
			if (not os.path.exists('upload/')):
				os.mkdir('upload/')
			if (os.path.exists('upload/image' + file_type)):
				os.remove('upload/image' + file_type)
			try:
				# Store the file from multi-part to Heroku Ephemeral File System
				with open('upload/image' + file_type, 'wb+') as destination:
					for chunk in file.chunks():
						destination.write(chunk)
				# Determine correct file name on S3
				s3 = boto3.resource('s3')
				path = easting + '/' + northing + '/' + context + '/' + sample + '/'
				imageNumber = 0
				for file in s3.Bucket(AWS_STORAGE_BUCKET_NAME).objects.filter(Prefix = path):
					number = int(file.key[file.key.rfind('/') + 1:file.key.find('.')])
					if (imageNumber < number):
						imageNumber = number
				# Store the image on S3
				# If the directory does not exist, will be added and count starts at 1
				path = path + str(imageNumber + 1) + file_name[file_name.find('.'):]
				data = open(file_name, 'rb')
				s3.Bucket(AWS_STORAGE_BUCKET_NAME).put_object(Key = path, Body = data)
				return HttpResponse("Upload Successful", 'test/plain')
			except (Exception, boto3.exceptions.S3UploadFailedError) as error:
				return HttpResponse("Error: Insertion failed", content_type = "text/plain")
			except (Exception, botocore.exceptions.ClientError):
				return HttpResponse("Error: Bucket does not exist or credentials are invalid", content_type = 'text/plain')
		else:
			logger.info('Invalid Form')
			form = UploadFileForm()
	logger.info('Redirecting request to blank form')
	return render(request, 'upload_image.html', {'form': form})

# Route for adding image to S3
# Param: request - HTTP client request
# Returns an HTML render
@csrf_exempt
def add_image(request):
	easting = request.GET.get('easting', '')
	northing = request.GET.get('northing', '')
	context = request.GET.get('context', '')
	sample = request.GET.get('sample', '')
	file_name = request.GET.get('file_name', '')
	# Should have already been checked but checking again in case its possible to call this method without upload_image first
	keyword = find_sql_keyword(file_name)
	try:
		int(easting)
	except ValueError:
		return HttpResponse('Provided area easting is not a number', content_type = 'text/plain')
	try:
		int(northing)
	except ValueError:
		return HttpResponse('Provided area northing is not a number', content_type = 'text/plain')
	try:
		int(context)
	except ValueError:
		return HttpResponse('Provided context number is not a number', content_type = 'text/plain')
	try:
		int(sample)
	except ValueError:
		return HttpResponse('Provided sample number is not a number', content_type = 'text/plain')
	if (keyword != ''):
		return HttpResponse('SQL keyword ' + keyword + ' not allowed in file_name', content_type = 'text/plain')
	s3 = boto3.resource('s3')
	path = easting + '/' + northing + '/' + context + '/' + sample + '/'
	try:
		imageNumber = 0
		for file in s3.Bucket(AWS_STORAGE_BUCKET_NAME).objects.filter(Prefix = path):
			number = int(file.key[file.key.rfind('/') + 1:file.key.find('.')])
			if (imageNumber < number):
				imageNumber = number
		# If the directory does not exist, will be added and count starts at 1
		path = path + str(imageNumber + 1) + file_name[file_name.find('.'):]
		data = open(file_name, 'rb')
		s3.Bucket(AWS_STORAGE_BUCKET_NAME).put_object(Key = path, Body = data)
	except FileNotFoundError:
		return HttpResponse('File ' + file_name + ' could not be found', content_type = 'text/plain')
	except (Exception, boto3.exceptions.S3UploadFailedError) as error:
		return HttpResponse("Error: Insertion failed", content_type = "text/plain")
	except (Exception, botocore.exceptions.ClientError):
		return HttpResponse("Error: Bucket does not exist or credentials are invalid", content_type = 'text/plain')
	return HttpResponse("File uploaded successfully", content_type = 'text/plain')

# Route for fetching image urls
# Param request - HTTP client request
# Returns an HTTP response
def get_image_urls(request):
	easting = request.GET.get('easting', '')
	northing = request.GET.get('northing', '')
	context = request.GET.get('context', '')
	sample = request.GET.get('sample', '')
	try:
		int(easting)
	except ValueError:
		return HttpResponse('Provided area easting is not a number', content_type = 'text/plain')
	try:
		int(northing)
	except ValueError:
		return HttpResponse('Provided area northing is not a number', content_type = 'text/plain')
	try:
		int(context)
	except ValueError:
		return HttpResponse('Provided context number is not a number', content_type = 'text/plain')
	try:
		int(sample)
	except ValueError:
		return HttpResponse('Provided sample number is not a number', content_type = 'text/plain')
	s3 = boto3.resource('s3')
	path = easting + '/' + northing + '/' + context + '/' + sample + '/'
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
		response = 'Error: database is empty'
	cursor.close()
	connection.close()
	return HttpResponse(response, content_type = 'text/plain')

# Get the eastings in the database
# Param: request - HTTP client request
# Returns an HTTP response
def get_area_eastings(request):
	connection = psycopg2.connect(host = hostname, user = username, password = password, dbname = database)
	cursor = connection.cursor()
	cursor.execute("SELECT DISTINCT area_easting FROM Samples WHERE status = 'active' ORDER BY area_easting ASC;")
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
	cursor.close()
	connection.close()
	return HttpResponse(response, content_type = 'text/html')

# Get the northings under a particular easting
# Param: request - HTTP client request
# Returns an HTTP response
def get_area_northings(request):
	easting = request.GET.get('easting', '')
	try:
		int(easting)
	except ValueError:
		return HttpResponse('<h3>Provided area_easting is not a number</h3>', content_type = 'text/html')
	connection = psycopg2.connect(host = hostname, user = username, password = password, dbname = database)
	cursor = connection.cursor()
	cursor.execute("SELECT DISTINCT area_northing FROM Samples WHERE status = 'active' AND area_easting = " + easting + " ORDER BY area_northing ASC;")
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
	cursor.close()
	connection.close()
	return HttpResponse(response, content_type = 'text/html')

# Get contexts within an easting and northing
# Param: request - HTTP client request
# Returns an HTTP response
def get_context_numbers(request):
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
	connection = psycopg2.connect(host = hostname, user = username, password = password, dbname = database)
	cursor = connection.cursor()
	query = "SELECT DISTINCT context_number FROM Samples WHERE status = 'active' AND area_easting = " + easting
	query = query + " AND area_northing = " + northing + " ORDER BY context_number ASC;"
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
	cursor.close()
	connection.close()
	return HttpResponse(response, content_type = 'text/html')

# Get sample numbers within an easting, northing, and context
# Param: request - HTTP client request
# Returns an HTTP response
def get_sample_numbers(request):
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
	connection = psycopg2.connect(host = hostname, user = username, password = password, dbname = database)
	cursor = connection.cursor()
	query = "SELECT sample_number FROM Samples WHERE status = 'active' AND area_easting = " + easting
	query = query + " AND area_northing = " + northing + " AND context_number = " + context + " ORDER BY sample_number ASC;"
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
	cursor.close()
	connection.close()
	return HttpResponse(response, content_type = 'text/html')

# Get a sample from the database
# Param: request - HTTP client request
# Returns an HTTP response
def get_sample(request):
	easting = request.GET.get('easting', '')
	northing = request.GET.get('northing', '')
	context = request.GET.get('context', '')
	sample = request.GET.get('sample', '')
	try:
		int(easting)
	except ValueError:
		return HttpResponse('Provided area_easting is not a number', content_type = 'text/plain')
	try:
		int(northing)
	except ValueError:
		return HttpResponse('Provided area_northing is not a number', content_type = 'text/plain')
	try:
		int(context)
	except ValueError:
		return HttpResponse('Provided context_number is not a number', content_type = 'text/plain')
	try:
		int(sample)
	except ValueError:
		return HttpResponse('<h3>Provided sample_number is not a number', content_type = 'text/plain')
	connection = psycopg2.connect(host = hostname, user = username, password = password, dbname = database)
	cursor = connection.cursor()
	query = "SELECT * FROM Samples WHERE status = 'active' AND area_easting = " + easting + " AND area_northing = " + northing
	query = query + " AND context_number = " + context + " AND sample_number = " + sample + ";"
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
	cursor.close()
	connection.close()
	return HttpResponse(response, content_type = 'text/plain')

# Set the weight of an object
# Param: request - HTTP client request
# Returns an HTTP response
def set_weight(request):
	easting = request.GET.get('easting', '')
	northing = request.GET.get('northing', '')
	context = request.GET.get('context', '')
	sample = request.GET.get('sample', '')
	weight = request.GET.get('weight', '')
	try:
		int(easting)
		int(northing)
		int(sample)
		int(context)
		float(weight)
	except ValueError:
		return HttpResponse("Error: One or more parameters are invalid", content_type = 'text/plain')
	connection = psycopg2.connect(host = hostname, user = username, password = password, dbname = database)
	cursor = connection.cursor()
	query = "UPDATE Samples SET weight_kilograms = " + weight + " WHERE area_easting = " + easting + " AND area_northing = "
	query = query + northing + " AND context_number = " + context + " AND sample_number = " + sample + ';'
	response = None
	try:
		cursor.execute(query)
		# Make sure the query updated a row
		if (cursor.rowcount == 1):
			response = HttpResponse("Update successful", content_type = 'text/plain')
		connection.commit()
	except (Exception, psycopg2.DatabaseError) as error:
		response = HttpResponse("Error: Object not found in Samples table", content_type = "text/plain")
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
	if (len(key) > 40 or len(value) > 100):
		return HttpResponse("Error: Max Key length = 40, Max Value length = 100", content_type = 'text/plain')
	keySQL = find_sql_keyword(key)
	valueSQL = find_sql_keyword(value)
	if (keySQL != ''):
		return HttpResponse("Error: SQL Keyword " + keySQL + " found in key", content_type = 'text/plain')
	elif (valueSQL != ''):
		return HttpResponse("Error: SQL Keyword " + valueSQL + " found in value", content_type = 'text/plain')
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
	if (keyword != ''):
		return HttpResponse("Error: SQL Keyword " + keyword + " found in key", content_type = 'text/plain')
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