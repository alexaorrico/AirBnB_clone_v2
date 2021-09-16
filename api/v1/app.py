#!/usr/bin/python3
"""
Contains the FileStorage class
"""
from flask import Flask
from models import storage
from api.v1.views import app_views
import getenv
app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(exception):
	"""Remove the current SQLAlchemy session"""
	storage.close()

if __name__ == "__main__":
	if getenv('HBNB_API_HOST'):
		host = getenv('HBNB_API_HOST')
	else:
		host = '0.0.0.0'
	if getenv('HBNB_API_PORT'):
		port = getenv('HBNB_API_PORT')
	else:
		port = 5000
	app.run(host=host, port=port, threaded=True)