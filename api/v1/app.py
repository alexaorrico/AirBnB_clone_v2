#!/usr/bin/python3
""" module for api """


import flask
from flask import Flask
from models import storage
from api.v1.views import app_views
import os
from flask import jsonify


app = Flask(__name__)
app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found(error):
    """ function for error 404 """
    response = jsonify({"error": "Not found"})
    response.status_code = 404
    return response


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


host_name = os.getenv("HBNB_API_HOST") if os.getenv("HBNB_API_HOST") else "0.0.0.0"
port_name = os.getenv("HBNB_API_PORT") if os.getenv("HBNB_API_PORT") else "5000"


if __name__ == '__main__':
    app.run(host=host_name, port=port_name, threaded=True)
