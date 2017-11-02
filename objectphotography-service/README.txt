Contains PHP scripts for retrieving and sending information to a database.
Database is saved in Properties.php, change as needed to fit your database.
ObjectPhotography app retrieves and sends via yourWebServerURL/web/appropriate_php_script.php i.e. http://localhost/web/test_service.php

The /web/php_script is set up in the Procfile (web/ at the end), change to the correct routing as desired.

To set up a web server with Heroku: https://devcenter.heroku.com/articles/getting-started-with-php#introduction