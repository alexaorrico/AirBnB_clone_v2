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
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/v1*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def storage_close(obj):
    """ Close Storage"""
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """Error 404"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main":
    auHost = getenv('HBNB_API_HOST') or '0.0.0.0'
    auPort = getenv('HBNB_API_PORT') or 5000

    app.run(host=auHost, port=auPort, threaded=True)
