#!/usr/bin/python3
"""
Module contains all api routes for the AirBnB clone project
"""

#from os import getenv
import os
from models import storage
from flask import Flask, jsonify
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(self):
    """
    Closes all sessions running in storage
    """
    storage.close()

@app.errorhandler(404)
def page_not_found(e):
    """handles the 404 error
    """
    status = {"error": "Not found"}
    return jsonify(status), 404

# Defaults
#default_host = "0.0.0.0"
#default_port = 5000

# Host and port configs
#host = getenv("HBNB_API_HOST", default_host)
#port = int(getenv("HBNB_API_PORT", default_port))


if __name__ == '__main__':
    try:
        host = os.environ.get('HBNB_API_HOST')
    except:
        host = '0.0.0.0'

    try:
        port = os.environ.get('HBNB_API_PORT')
    except:
        port = '5000'
    app.run(host=host, port=port, threaded=True)
