#!/usr/bin/python3
""" start a flask application """

from flask import Flask, make_response
from models import storage
from api.v1.views import app_views
from os import getenv
import json
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown(ret):
    """ call storage.close method """
    storage.close()

if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', 5000)
    app.run(host=host, port=port, threaded=True)
