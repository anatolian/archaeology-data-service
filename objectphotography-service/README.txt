Contains PHP scripts for retrieving and sending information to a database.



Database information is saved in Properties.php, change as needed to fit your database.
Archaeology app retrieves and sends via yourWebServerURL/appropriate_php_script.php i.e. http://localhost/test_service.php

The php_script routing is set up in the Procfile (at the end), change to the correct routing as desired.
For example, nothing at the end means http://localhost/test_service.php, but web/ at the end means http://localhost/web/test_service.php

This can allow you to clean up your top directory, or add additional folders for other things, such as other folders for files, while keeping the PHP scripts separate for easy access.


The scripts are currently being saved in the top directory and can be called by appending their names to the end. 
For example: https://localhost/test_service.php is a script that checks a table in the database that is never empty, and returns whether or not a connection has been made.
Some scripts require arguments in order to run.
For example: https://localhost/get_area_northing.php?area_easting=10
or
https://localhost/get_sample_number.php?area_easting=10&area_northing=20&context_number=1

As it is currently a server made solely for the app to call scripts, there are no views, and most links on the server will return a blank page or returning JSON strings or arrays that contain the information called from the script.


To set up a web server with Heroku: https://devcenter.heroku.com/articles/getting-started-with-php#introduction.

The current files should allow for easy setup, just add the files and the server should be up and running.



The database being used is a PostgreSQL database set up via Heroku, attached to a Heroku acccount.
This information is saved in Properties.php and used by the scripts to set up a connection.

To set up a PostgreSQL database with Heroku: https://devcenter.heroku.com/articles/heroku-postgresql#provisioning-heroku-postgres

You can connect to the database to set up tables and schemas via terminal/cmd prompt with:
	psql -h HOST -U USER DATABASE_NAME 
where HOST, USER, and DATABASE_NAME can be found in Heroku's PostgreSQL properties.
