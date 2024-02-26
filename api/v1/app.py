#!/usr/bin/python3
""" API app module """

import os
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS


app = Flask(__name__)

host = "0.0.0.0"
port = 5000

cors = CORS(app, resources={r'/*': {'origins': host}})


@app.teardown_appcontext
def teardown(exception):
    """ Teardown  function """
    storage.close()


@app.errorhandler(404)
def not_found_error(error):
    """ returns a JSON-formatted 404 status code response """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    if 'HBNB_API_HOST' in os.environ:
        host = os.environ["HBNB_API_HOST"]
    if "HBNB_API_PORT" in os.environ:
        port = int(os.environ["HBNB_API_PORT"])
    app.register_blueprint(app_views)
    app.run(host=host, port=port, threaded=True)
