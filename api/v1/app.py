#!/usr/bin/python3
"""API app construction"""
import os
from flask import Flask
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.register_bluprint(app_views)


@app.teardown_appcontext
def teardown():
    """Teardown app"""
    storage.close()


if __name__ == '__main__':
    hostvar = '0.0.0.0'
    portvar = '5000'
    if os.getenv('HBNB_API_HOST'):
        hostvar = os.getenv('HBNB_API_HOST')
    if os.getenv('HBNB_API_PORT'):
        portvar = os.getenv('HBNB_API_PORT')

    app.run(host=hostvar, port=portvar, threaded=True)
