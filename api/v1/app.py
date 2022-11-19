#!/usr/bin/python3

"""
This module is responsible for setting up the environment for the API
"""

from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)

host = getenv('HBNB_API_HOST', '0.0.0.0')
port = getenv('HBNB_API_PORT', 5000)

@app.teardown_appcontext
def teardown_sess(Exception):
    """
    Function to terminate db session after each request
    """
    storage.close()

if __name__ == "__main__":
    """Main app to run from console"""
    app.run(host=host, port=port, threaded=True)
