#!/usr/bin/python3
"""
Flask App that integrates with AirBnB static HTML Template
"""
from flask import Flask, render_template, url_for, Blueprint
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)


# get host and ports and register app_views
host = os.getenv('HBNB_API_HOST', '0.0.0.0')
port = os.getenv('HBNB_API_PORT', 5000)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


# Declare a method to handle @teardown_appcontext that calls storage.close()
@app.teardown_appcontext
def teardown_db(exception):
    """
     Teardown the database after each request.

     This function is registered to Flask's teardown_appcontext decorator.
     It closes the database connection after each request.

     :param exception: The exception object, if any.
    """

    storage.close()


if __name__ == "__main__":

   # run flask app with environment variables and options
    app.run(host=host, port=port)
