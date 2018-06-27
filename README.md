# Archaeology Service:
Contains Python scripts for retrieving and sending information to a database.
You will need to create a Heroku webapp to host the service onto.

## Dependencies
You will need the following installed on your machine:
- Python 3.6+ (preferably the newest version in case dependencies become depricated)
- PostgreSQL
- pip

## Heroku - Running Locally

Make sure you have Python installed properly (http://install.python-guide.org). Also, install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) and
[Postgres](https://devcenter.heroku.com/articles/heroku-postgresql#local-setup).

Note also that running locally reads from environment variables. Please be sure to set the postgres_username, postgres_password, postgres_database, and postgres_hostname
variables corresponding to the PostgreSQL connection parameters. See Section PostgreSQL below for more details.

```sh
$ pipenv install
$ python manage.py migrate
$ python manage.py collectstatic
$ heroku local
```

Your app should now be running on [localhost:5000](http://localhost:5000/). Note, deploying locally can help debug setup issues, but to actually communicate with the Android
app you will need to deploy to a proper web service (i.e. Heroku). See the next section once local deployment works.

## PostgreSQL
To set up a PostgreSQL database with Heroku: https://devcenter.heroku.com/articles/heroku-postgresql#provisioning-heroku-postgres.
This will attach your database to a Heroku app, but may be accessed outside of this app.
From terminal/cmd prompt, with Postgres set up: psql -h HOST -U USER PASS,
where HOST, USER, and PASS can be found in your Heroku properties if you're using Heroku.
You can also access a database created outside of Heroku the same way.

The server can be accessed via https://[serverURL].com
The scripts are currently being saved in the top directory and can be called by appending their names to the end with the correct routing.
For example, with scripts in the top level directory https://[serverURL].com/relations is a script that checks for the presense of tables,
	and returns whether or not a connection has been made.

Note: Some scripts require GET parameters in order to run.
For example, with scripts in the top level directory: - https://[serverURL].com/get_northings/?easting=10
	or - https://[serverURL].com/get_samples/?easting=10&northing=20&context=1

This server also has very basic views, so navigating to the corresponding URL of a route will display a server response, sometimes an HTML page with links,
	but plaintext for other calls.

## Deploying to Heroku

Before deploying to Heroku for the first time, you must send your required environment variables to it through the following commands:

```sh
$ heroku config:set postgres_username=zzz
$ heroku config:set postgres_password=ppp
$ heroku config:set postgres_database=ddd
$ heroku config:set postgres_hostname=hhh
```

The service directory must be a git repository for Heroku to accept it. If you cloned this project you should be good to go. Otherwise, you'll need to deploy it to a git service (e.g. bitbucket, GitHub, gitlab, etc). Then deploy the app through the following:

```sh
$ heroku create
$ git push heroku master
$ heroku run python manage.py migrate
$ heroku open
```

# LICENSE

The use of this project is governed by the license found [here](https://github.com/anatolian/archaeology-object-data-collector-service/blob/master/LICENSE)
