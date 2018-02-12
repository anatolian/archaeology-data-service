# Archaeology Service:
Contains Python scripts for retrieving and sending information to a database.
You will need to create either an Amazon EC2 instance or a Heroku webapp to host the service onto.
Additionally, you will need to create an Amazon S3 bucket to store images onto.

## Dependencies
You will need the following installed on your machine:
	Python 3.6+ (preferably the newest version in case dependencies become depricated)
	PostgreSQL
	pip
	boto3 (pip install boto3)
	flask (pip install flask)
	django (pip install django)

## You may use an Amazon EC2 instance:
For instructions on launching an EC2 instance: https://aws.amazon.com/ec2/getting-started/.
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

## Heroku - Running Locally

Make sure you have Python [installed properly](http://install.python-guide.org). Also, install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) and
[Postgres](https://devcenter.heroku.com/articles/heroku-postgresql#local-setup).

Note also that running locally reads from environment variables. Please be sure to set the postgres_username, postgres_password, postgres_database, and postgres_hostname
variables corresponding to the PostgreSQL connection parameters. See Section PostgreSQL below for more details. Also be sure to store the AWSAccessKeyId, AWSSecretKey
and S3_BUCKET_NAME from Section Amazon S3 below.

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

Before deploying to Heroku for the first time, you must send your required environment variables to it through the following command:

```sh
$ heroku config:set AWS_ACCESS_KEY_ID=xxx AWS_SECRET_ACCESS_KEY=yyy postgres_username=zzz postgres_password=ppp postgres_database=ddd postgres_hostname=hhh S3_BUCKET_NAME=bbb
```

Then deploy the app through the following:

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
For example, with scripts in the top level directory: https://<serverURL>.com/relations is a script that checks for the presense of tables,
	and returns whether or not a connection has been made.
- Some scripts require arguments in order to run.
For example, with scripts in the top level directory: https://<serverURL>.com/get_northings/?easting=10
or https://<serverURL>.com/get_samples/?easting=10&northing=20&context=1

This server also has very basic views, so navigating to the corresponding URL of a route will display a server response, sometimes an HTML page with links,
	but plaintext for other calls.

## Amazon S3
For instructions on how to create an S3 bucket, see this page: https://devcenter.heroku.com/articles/s3
Once the bucket is created, connect it to Heroku through the following tutorial: https://devcenter.heroku.com/articles/s3-upload-python
(this page lists different environment variable names than Amazon does, stick with Amazon's)

# LICENSE

The use of this project is governed by the license found [here](https://github.com/anatolian/archaeology-object-data-collector-service/blob/master/LICENSE)