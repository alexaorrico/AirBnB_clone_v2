#!/usr/bin/python3'
""" App Module """


from models import storage
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify, abort
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)
app.config.update(JSONIFY_PRETTYPRINT_REGULAR=True)


@app.errorhandler(404)
def not_found(e):
    """ Returns a 404 error in JSON format """
    return jsonify({"error": "Not found"}), 404


@app.teardown_appcontext
def teardown(close):
    ''' Closes current storage session '''
    storage.close()


if __name__ == "__main__":
    hosts = getenv("HBNB_API_HOST", default='0.0.0.0')
    ports = int(getenv("HBNB_API_PORT", default=5000))
    app.run(host=hosts, port=ports, threaded=True)
