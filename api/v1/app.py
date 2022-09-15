#!/usr/bin/python3
""" Module for start the API """

from flask import Flask 
from models import storage
from api.v1.views import app_views
from os import getenv



app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown_appcontext():
    """call method to close"""
    storage.close()

if __name__ == "__main__":
    host_env = getenv('HBNB_API_HOST')
    port_env = getenv('HBNB_API_PORT')
    if not host_env:
        host = "0.0.0.0"
    if not port_env:
        port = 5000
    app.run(host=host_env, port=int(port_env), threaded=True)
