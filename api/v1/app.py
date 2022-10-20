#!/usr/bin/python3
"""
This is the first AirBnB clone RESTful API Flask application
How to use:
    > export FLASK_APP=app.py
    > flask run
"""
from flask import Flask
from models import storage
from api.v1.views import app_views
import os

# create instance of Flask app
app = Flask(__name__)

# Register app_views to flask instance
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown_appcontext:
    storage.close()

if __name__ == "__main__":
    # get environment variables and run flask
    app.run(os.getenv('HBNB_API_HOST', '0.0.0.0'), os.getenv('HBNB_API_PORT', 5000), threaded=True)
