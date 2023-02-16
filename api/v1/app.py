#!/usr/bin/python3

"""
Entry point for flask
"""

from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)
app.url_map.strict_slashes = False
cors = CORS(app, resources={"*": {"origins": "0.0.0.0"}})

ip = getenv("HBNB_API_HOST") or '0.0.0.0'
port = getenv("HBNB_API_PORT") or 5000


@app.errorhandler(404)
def resource_not_found(e):
    """ throws 404 error on bad routes """
    return jsonify({"error": "Not found"}), 404


@app.teardown_appcontext
def teardown(self):
    """ tears down app context """
    storage.close()


if __name__ == '__main__':
    app.run(host=ip, port=port, threaded=True)
