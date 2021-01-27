#!/usr/bin/python3
""" Status of our API """
from models import storage
from api.v1.views import app_views
from os import getenv
from flask import Flask

"""Host and port env variables"""
host_env = getenv('HBNB_API_HOST') or '0.0.0.0'
port_env = getenv('HBNB_API_PORT') or 5000

app = Flask(_name__)

@app.teardown_appcontext
def teardown_db(error):
    """ Close db session """
    storage.close()

if __name__ == "__main__":
    app.run(
        host=host_env, port=port_env,
        debug=True, threaded=True,
    )
