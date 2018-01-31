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