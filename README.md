#UoG Mobile API
This is the server component of the UoG Mobile application. Its built using [Flask](flask.pocoo.org) and uses [Selenium's](https://github.com/seleniumhq/selenium) [Python API](selenium-python.readthedocs.org) to scrape the University's various web services.

##Installation
The only installation requirement for the application is Docker so you should use their [install instructions](https://docs.docker.com/engine/installation/) for your OS.

Once Docker is installed you need to create a ```config.py``` in the root directory for Flask to load. You can use any [configuration values](http://flask.pocoo.org/docs/0.10/config/#builtin-configuration-values) you like but a ```SECRET_KEY``` is required. Here's a sample config file.

```
DEBUG=True
SECRET_KEY="you should generate me"
```

You can easily generate a ```SECRET_KEY``` by running the following in your Python REPL and copying the output to the config file
```
import os
os.urandom(24)
```

##Running and other important commands
```
# Start the servers in Docker's daemon mode
docker-compose up -d

# Check status of the servers
docker-compose ps

# Stop the servers if they're running
docker-compose stop

# Run the unit tests
docker-compose run web python3 -m unittest -v
```
*Note all of these commands are run from the root of the project directory*

##Contributing
For more information on the project structure and extending the functionality checkout the wiki
