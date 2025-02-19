#!/usr/bin/python3
"""
Starts AirBnB Flask main application
"""

from flask import Flask
from models import storage
from app.v1.views import app_views
from os import getenv

API_HOST = getenv('HBNB_API_HOST', '0.0.0.0')
API_PORT = getenv('HBNB_API_PORT', 5000)

app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def close_api(exception):
	""" Closes storage if we encounter an exception """
	storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """returns a status code response"""
    return jasonify("error": "Not found"), 404


if __name__ == "__main__":
	app.run(host=API_HOST, port=API_PORT, threaded=True)
