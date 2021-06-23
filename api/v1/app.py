#!/usr/bin/python3
""" Setup API """
from flask import Flask, escape, request, render_template, Blueprint, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS, cross_origin


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": '0.0.0.0'}})
app.register_blueprint(app_views)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.teardown_appcontext
def teardown(context):
    """ will only run when app is done """
    storage.close()


@app.errorhandler(404)
def error404(e):
    """ Will return a 404 error """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST')
    port = getenv('HBNB_API_PORT')
    if host is None:
        host = '0.0.0.0'
    if port is None:
        port = '5000'
    app.run(host=host, port=port, threaded=True)
