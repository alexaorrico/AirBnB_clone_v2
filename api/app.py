#!usr/bin/python3
'''
AirBnB API
'''

from os import getenv
from flask import Flask, Blueprint, jsonify
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontex
def teardown_close():
    '''
    Teardown cose calls close method
    '''
    storage.close()

if __name__ == "__main__":
    '''
    Run app with host and port environment variables, if none use default
    '''

    if (host is None):
        host = 0.0.0.0
    else:
        host = getenv('HBNB_API_PORT')

    if (port is None):
        port = 5000
    else:
        port = getenv('HBNB_API_PORT')

    app.run(host, threaded=True)
