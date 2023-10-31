#!/usr/bin/python3
"""
This file contains the RESTFUL API
"""
from models import storage
from api.v1.views import app_views
from flask import Flask, make_response, jsonify
from os import getenv
from flask_cors import CORS
from flasgger import Swagger

app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def storage_close(obj):
  """ Close Storage"""
    storage.close()

if __name__ == "__main":
   host = getenv('HBNB_API_HOST', default='0.0.0.0')
   port = getenv('HBNB_API_PORT', default=5000)
   app.run(host, int(port), threaded=True)
