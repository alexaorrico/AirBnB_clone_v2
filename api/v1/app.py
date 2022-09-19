#!/usr/bin/python
""" flask framwork"""
from flask import Flask, abort

from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(error):
    """ calls storege.close to close
    sqlalqemy """
    storage.close()


@app.errorhandler(404)
def not_found(e):
    """ handle errors"""
    error_404 = {"error": "Not found"}
    return error_404, 404


if __name__ == "__main__":
    """ run fask app"""
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True)
