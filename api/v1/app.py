#!/usr/bin/python3
"""
starts a Flask web application
"""

from api.v1.views import app_views
from flask import Flask
from models import storage
import os

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def tearthisdown():
    storage.close()

if __name__ == "__main__":
    thisHost = os.getenv('HBNB_API_HOST')
    thisPort = os.getenv('HBNB_API_PORT')
    if thisHost is None:
        thisHost = '0.0.0.0'
    if thisPort is None:
        thisPort = '5000'
    app.run(host=thisHost, port=thisPort, threaded=True)
