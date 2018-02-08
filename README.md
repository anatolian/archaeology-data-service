# Archaeology Service:
Contains PHP scripts for retrieving and sending information to a database.
Database is saved in Archaeology/web/Properties.php.

## You may use an Amazon EC2 instance:
You will need to create an Amazon EC2 instance to connect to: https://aws.amazon.com/ec2/getting-started/.
- Make sure to open port 5432 to all traffic.
- Make sure to create a key pair and download it to your machine. Either store the .pem outside of the project directory or add it
	to the .gitignore. NEVER PUSH THE .pem FILE!
- You will need to copy the contents of the Archaeology service directory (NOT the directory itself) to the EC2 instance.
	- MAC/LINUX users can use scp through Terminal.
	- Windows users with Bash installed (https://git-scm.com/downloads) can use scp, otherwise, use FileZilla (https://filezilla-project.org/)
- Once the EC2 instance is launched, in Properties.php, replace:
	- The value of PG_HOST with the EC2 instance's Public DNS (IPv4), found on the EC2 console.
	- The value of PG_DB with the EC2 DB name.
	- The value of PG_USERNAME with the EC2 account associated with the DB.
	- The value of PG_PASSWORD with the DB password.
	- The value of TEST_BASE_IMAGE_URL with the EC2 IPv4 Public IP.
	- NOTE: NEVER PUSH THESE VALUES TO ANY REPOSITORY. Alternatively, if you make PG_HOST, PG_DB, PG_USERNAME, and PG_PASSWORD
		read from environment variables, you can push this file.

Archaeology app retrieves and sends via yourWebServerURL/web/appropriate_php_script.php
	i.e. http://ec2-XX-XXX-XX-XX.compute-1.amazonaws.com/web/test_service.php

The /web/php_script is set up in the Procfile (web/ at the end), change to the correct routing as desired.

## Heroku
To set up a web server with Heroku: https://devcenter.heroku.com/articles/getting-started-with-php#introduction.
The files in this repo have been set up with Heroku and should be able to be deployed and ready to go.

## Running Locally

Make sure you have Python [installed properly](http://install.python-guide.org). Also, install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) and [Postgres](https://devcenter.heroku.com/articles/heroku-postgresql#local-setup).

```sh
$ git clone git@github.com:heroku/python-getting-started.git
$ cd python-getting-started

$ pipenv install

$ createdb python_getting_started

$ python manage.py migrate
$ python manage.py collectstatic

$ heroku local
```

Your app should now be running on [localhost:5000](http://localhost:5000/).

## Deploying to Heroku

```sh
$ heroku create
$ git push heroku master

$ heroku run python manage.py migrate
$ heroku open
```
or

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

## PostgreSQL
To set up a PostgreSQL database with Heroku: https://devcenter.heroku.com/articles/heroku-postgresql#provisioning-heroku-postgres.
This will attach your database to a Heroku app, but may be accessed outside of this app.
From terminal/cmd prompt, with Postgres set up: psql -h HOST -U USER PASS,
where HOST, USER, and PASS can be found in your Heroku properties if you're using Heroku.
You can also access a database created outside of Heroku the same way.

The server can be accessed via https://<serverURL>.com
The scripts are currently being saved in the top directory and can be called by appending their names to the end with the correct routing.
For example, with scripts in the top level directory: https://<serverURL>.com/test_service.php is a script that checks a table in the database that is never empty,
	and returns whether or not a connection has been made.
- Some scripts require arguments in order to run.
For example, with scripts in the top level directory: https://<serverURL>.com/get_area_northing.php?area_easting=10
or https://<serverURL>.com/get_sample_number.php?area_easting=10&area_northing=20&context_number=1

As it is currently a server made solely for the app to call scripts, there are no views, and most links on the server will return a blank page or returning JSON
	strings or arrays that contain the information called from the script.

# LICENSE

The use of this project is governed by the license found [here](https://github.com/anatolian/archaeology-object-data-collector-service/blob/master/LICENSE)