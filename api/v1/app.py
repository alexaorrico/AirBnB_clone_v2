#!/usr/bin/python3
"""A Flask API server that controls error and variables
    of API host_IP and Port
"""


from flask import Flask, jsonify
from models import storage
from os import getenv
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def downtear(self):
    """teardown app and terminate the session"""
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """return page not found (code)
    Arg:
        error: error variable

    Return:
        JSON
    """
    return jsonify({"error": 'Not found'}), 404


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST')
    port = getenv('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, threaded=True)
